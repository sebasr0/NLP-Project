import os
import pandas as pd
import json
from groq import Groq
import sys
import time  # Import time for sleep during debugging (optional)

class ComplaintGenerator:
    def __init__(self, api_key, themes, max_requests=5000, chunk_size_gb=2):
        self.api_key = api_key
        self.themes = themes
        self.max_requests = max_requests
        self.chunk_size_bytes = chunk_size_gb * 1024 ** 3  # Convert GB to bytes
        self.client = Groq(api_key=self.api_key)
        self.total_requests = 0
        self.complaints_data = []
        self.chunk_counter = 1
        self.current_data_size = 0  # Initialize current data size in bytes

    def generate_complaint(self, theme, last_complaint=None):
        """
        Generates a bank complaint using the Groq API.

        Parameters:
            theme (str): Theme of the complaint (e.g., "credit cards", "mortgage loans", etc.)
            last_complaint (str, optional): The last complaint generated, to avoid repetition.

        Returns:
            str: The generated complaint. If there was an error making the request, returns None.
        """
        if self.total_requests >= self.max_requests:
            raise Exception("Maximum number of requests reached.")

        # Build the base prompt
        prompt = (
            f"Generate a new and unique realistic for JPMorgan Chase bank complaint about {theme}. "
            "The complaint should come from a customer, bank user, family member, or friend of the bank user with a random name. "
            "Include specific customer concerns and impacts. "
            "Vary the tone to reflect different customer, bank user, family member, friend, or lawyer of the bank customer experiences such as polite, frustrated, urgent, neutral, or happy, etc. "
            "Ensure the complaint is different from the previous one and begins with a different sentence. "
            "Limit the response to one paragraph without labels or quotation marks."
        )

        # If there is a last complaint, include it to avoid repetition
        if last_complaint:
            prompt += f"\n\nPrevious complaint to avoid repetition, be sure to begin with a different sentence:\n{last_complaint}"

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are to generate unique and realistic JPMorgan Chase bank complaints about specific topics. "
                            "Adjust the tone to reflect different customer, bank user, family member, friend, or lawyer of the bank user experiences such as polite, frustrated, urgent, neutral, happy, etc. "
                            "Each complaint should be a single paragraph of realistic customer feedback. "
                            "Do not repeat or paraphrase the previous complaint and make sure the complaint begins with a different sentence. "
                            "Limit the response to 300 tokens without labels or extra formatting."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-8b-instant",
                max_tokens=300,
                temperature=0.95,       # Increased temperature for more randomness
                top_p=0.8,            # Using nucleus sampling to increase diversity
                frequency_penalty=1, # Discourage repetition
                presence_penalty=1,  # Encourage new topics
            )
            # Extract the generated complaint text
            complaint_text = chat_completion.choices[0].message.content.strip()
            self.total_requests += 1
            return complaint_text if complaint_text else None

        except Exception as e:
            # You might want to log the exception to a file instead of printing
            # to avoid saturating the console
            # For now, we'll pass to avoid console output
            pass
            return None

    def get_size_in_bytes(self, s):
        return len(s.encode('utf-8'))

    def generate_complaints(self):
        """
        Generates complaints for all themes.
        """
        total_themes = len(self.themes)
        for theme_index, theme in enumerate(self.themes, start=1):
            last_complaint = None
            num_samples_per_theme = self.max_requests // len(self.themes)
            for sample_index in range(1, num_samples_per_theme + 1):
                if self.total_requests >= self.max_requests:
                    print("\nReached maximum number of requests.")
                    return
                complaint_text = self.generate_complaint(theme, last_complaint)
                if complaint_text:
                    complaint_data = {"theme": theme, "complaint": complaint_text}
                    self.complaints_data.append(complaint_data)
                    last_complaint = complaint_text  # Update the last complaint

                    # Update current data size
                    complaint_size = self.get_size_in_bytes(complaint_data['theme']) + self.get_size_in_bytes(complaint_data['complaint'])
                    self.current_data_size += complaint_size

                    # Check data size and save if chunk size exceeded
                    if self.current_data_size >= self.chunk_size_bytes:
                        self.save_data_chunk()

                    # Debugging: Update progress in the same line
                    progress_message = (
                        f"Theme {theme_index}/{total_themes}: '{theme}' | "
                        f"Sample {sample_index}/{num_samples_per_theme} | "
                        f"Total Requests: {self.total_requests}/{self.max_requests}"
                    )
                    sys.stdout.write('\r' + progress_message)
                    sys.stdout.flush()
                    # Optional: Sleep for a short time to see the update effect (remove in production)
                    # time.sleep(0.1)
                else:
                    # If no complaint was generated, skip updating progress to avoid confusion
                    pass
        # Move to the next line after completion
        print()

    def save_data_chunk(self):
        """
        Saves the current complaints data into a Parquet file and resets the data.
        """
        try:
            df = pd.DataFrame(self.complaints_data)
            filename = f"complaints_data_chunk_{self.chunk_counter}.parquet"
            df.to_parquet(filename, index=False)
            print(f"\nSaved chunk {self.chunk_counter} with {len(df)} complaints to {filename}")
            self.chunk_counter += 1
            self.complaints_data = []
            self.current_data_size = 0
        except Exception as e:
            # You might want to log the exception to a file instead of printing
            # to avoid saturating the console
            pass

    def run(self):
        try:
            self.generate_complaints()
        except Exception as e:
            # Log the exception instead of printing
            pass
        finally:
            # Save any remaining data
            if self.complaints_data:
                self.save_data_chunk()
            print("Generation process completed.")

if __name__ == "__main__":
    themes = [
        "Mortgage Loans and Properties",
        "Banking and Branch Operations",
        "Credit Reports and Consumer Protection",
        "Credit Cards and Financial Charges",
        "Fraud and Transaction Disputes"
    ]
    api_key = "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"  # Replace with your actual API key
    generator = ComplaintGenerator(api_key=api_key, themes=themes)
    generator.run()
