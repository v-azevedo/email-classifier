# Email Classifier - ClassifyAI

ClassifyAI is an advanced email classification tool that leverages machine learning algorithms to automatically categorize incoming emails into predefined categories. This helps users manage their inbox more efficiently and prioritize important messages.

## Features

- **Automatic Email Classification**: ClassifyAI uses natural language processing (NLP) techniques to analyze email content and assign appropriate classifications.
- **Generate Custom Replies**: ClassifyAI can generate personalized email replies based on the context and content of incoming messages.

## Limitations

While ClassifyAI is a powerful tool, it does have some limitations:

- **Rate Limiting**: Limited amount of allowed requests per user, maximum of 20 requests per day.
- **Privacy Concerns**: Users should be aware of privacy implications when using AI tools to process sensitive email content.

## How To Use ClassifyAI

1. **Clone the Repository**: Start by cloning the ClassifyAI repository from GitHub:

   ```bash
   git clone https://github.com/yourusername/email-classifier.git
   cd email-classifier
   ```

2. **Install the Required Libraries**: Ensure you have Python and Node.js installed along with the necessary libraries. You can install the required libraries using pip:

   ```bash
   cd classifier-api
   pip install -r requirements.txt
   cd classifier-ui
   npm install
   ```

3. **Set Up Environment Variables API**: Create a `.env` file in the `classifier-api` directory and add your Gemini API key:

   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Set Up Environment Variables UI**: Create a `.env` file in the `classifier-ui` directory and add your DEV_URL for the API:

   ```plaintext
    VITE_PROD_URL=hosted_url
    VITE_DEV_URL=local_url
   ```

5. **Start the Development Server**: Navigate to the `classifier-ui` and `classifier-api` directories and start the development servers:

   ```bash
   cd classifier-ui
   npm run dev
   cd ../classifier-api
   fastapi dev main.py
   ```

6. **Access the Application**: Open your web browser and navigate to `http://localhost:5000` to access the ClassifyAI user interface.

## Dependencies

ClassifyAI requires the following dependencies:

- Python 3.10 or higher
- Node.js 14 or higher
- FastAPI
- Pydantic
- Google-genai
- Python-multipart
- Pypdf
- Clsx
- Axios
- React
- Tailwind CSS
- React Icons
- React Spinners
- React Toastify
