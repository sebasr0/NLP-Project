from pyspark.sql import functions as F
from pyspark.sql.functions import udf, col, concat_ws, split
from pyspark.sql.types import ArrayType, StringType
from sparknlp.base import DocumentAssembler, Finisher
from sparknlp.annotator import Tokenizer, LemmatizerModel, PerceptronModel, StopWordsCleaner, NGramGenerator
from pyspark.ml import Pipeline, Transformer
from pyspark.ml.feature import CountVectorizerModel, IDFModel
from pyspark.ml.classification import LogisticRegressionModel
import re

# Text cleaning function
def clean_text_spark(spark, df, text_column):
    df = df.withColumn(text_column, F.lower(F.col(text_column)))
    df = df.withColumn(text_column, F.regexp_replace(F.col(text_column), r'\[.*?\]', ''))
    df = df.withColumn(text_column, F.regexp_replace(F.col(text_column), r'[^\w\s]', ''))
    df = df.withColumn(text_column, F.regexp_replace(F.col(text_column), r'\b\w*\d\w*\b', ''))
    df = df.withColumn(text_column, F.trim(F.col(text_column)))
    return df

# Define UDF to remove "xxxx" and extra spaces
def remove_xxxx(text):
    return re.sub(r"\s*xxxx\s*", "", text)

remove_xxxx_udf = udf(remove_xxxx, StringType())

# Lazy load models and transformers
def load_models(spark):
    count_vectorizer_model = CountVectorizerModel.load("/home/ubuntu/Documents/NLP-Project/models/count_vectorizer_model")
    idf_model = IDFModel.load("/home/ubuntu/Documents/NLP-Project/models/idf_model")
    logistic_regression_model = LogisticRegressionModel.load("/home/ubuntu/Documents/NLP-Project/models/logisticregression")

    # Define Spark NLP pipeline components and processing pipeline
    document_assembler = DocumentAssembler().setInputCol("complaint_what_happened").setOutputCol("document")
    tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
    stop_words_cleaner = StopWordsCleaner().setInputCols(["token"]).setOutputCol("cleanTokens").setCaseSensitive(False)
    lemmatizer = LemmatizerModel.pretrained().setInputCols(["cleanTokens"]).setOutputCol("lemmaTokens")
    ngram = NGramGenerator().setN(2).setInputCols(["lemmaTokens"]).setOutputCol("bigrams")
    pos_tagger = PerceptronModel.pretrained().setInputCols(["document", "lemmaTokens"]).setOutputCol("pos")
    finisher = Finisher().setInputCols(["lemmaTokens", "bigrams", "pos"]).setOutputCols(["finished_lemma", "finished_bigrams", "finished_pos"]).setCleanAnnotations(False)

    # Custom Transformer for POS extraction
    class POSExtractor(Transformer):
        def __init__(self, inputColPOS=None, inputColLemma=None, outputCol=None):
            super(POSExtractor, self).__init__()
            self.inputColPOS = inputColPOS
            self.inputColLemma = inputColLemma
            self.outputCol = outputCol

        def _transform(self, dataset):
            def extract_pos(pos_tags, lemmas):
                allowed_tags = ['NN', 'JJ', 'VB', 'RB']
                return [lemma for pos, lemma in zip(pos_tags, lemmas) if pos in allowed_tags]

            extract_pos_udf = udf(extract_pos, ArrayType(StringType()))
            return dataset.withColumn(self.outputCol, extract_pos_udf(col(self.inputColPOS), col(self.inputColLemma)))

    pos_extractor = POSExtractor(inputColPOS="finished_pos", inputColLemma="finished_lemma", outputCol="selected_tokens")

    # Custom Transformer to combine unigrams and bigrams
    class CombineUnigramsBigrams(Transformer):
        def __init__(self, inputColUnigrams=None, inputColBigrams=None, outputCol=None):
            super(CombineUnigramsBigrams, self).__init__()
            self.inputColUnigrams = inputColUnigrams
            self.inputColBigrams = inputColBigrams
            self.outputCol = outputCol

        def _transform(self, dataset):
            return dataset.withColumn(
                self.outputCol,
                split(
                    concat_ws(" ", col(self.inputColUnigrams), concat_ws(" ", col(self.inputColBigrams))),
                    " "
                )
            )

    combine_unigrams_bigrams = CombineUnigramsBigrams(inputColUnigrams="selected_tokens", inputColBigrams="finished_bigrams", outputCol="all_tokens")

    # Create preprocessing pipeline
    preprocessing_pipeline = Pipeline(stages=[
        document_assembler,
        tokenizer,
        stop_words_cleaner,
        lemmatizer,
        ngram,
        pos_tagger,
        finisher,
        pos_extractor,
        combine_unigrams_bigrams,
        count_vectorizer_model,
        idf_model
    ])

    # Full pipeline including classification model
    pipeline = Pipeline(stages=[preprocessing_pipeline, logistic_regression_model])
    return pipeline.fit(spark.createDataFrame([[""]], ["complaint_what_happened"]))

# Export necessary functions and UDFs, and defer pipeline loading
__all__ = ["clean_text_spark", "remove_xxxx_udf", "load_models"]
