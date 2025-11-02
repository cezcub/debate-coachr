# Debate Coachr AI

An AI-powered coaching tool for high school public forum debate teams. Provides detailed feedback on debate cases, transcriptions, and performance analysis using Azure OpenAI GPT-4.

## Features

- **Case Analysis**: Upload debate cases in multiple formats (TXT, DOCX, PDF) and receive detailed feedback
- **Transcription Analysis**: Analyze debate round recordings for strategic feedback
- **Multiple Upload Formats**: 
  - **Plaintext**: Standard text analysis
  - **Card Format**: Specialized analysis for structured debate cards with evidence
- **AI-Powered Feedback**: Comprehensive analysis covering content, strategy, evidence quality, and improvement suggestions

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **AI**: Azure OpenAI GPT-4
- **File Processing**: python-docx, PyPDF2
- **Deployment**: Azure Container Apps with managed identity

## Project Structure

```
OutreachAI/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (not in repo)
├── backend/
│   ├── azure.py               # Azure OpenAI integration
│   ├── case.py                # Case analysis FastAPI endpoints
│   ├── text_extraction.py     # File processing utilities
│   └── transcription.py       # Transcription analysis endpoints
├── frontend/
│   ├── case.py                # Case analysis UI
│   ├── chat.py                # Chat interface
│   └── pf_feedback.py         # Transcription feedback UI
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile         # Container configuration
│   │   └── docker-compose.yml
│   └── azure/                 # Azure deployment scripts
├── docs/                      # Documentation
└── .github/workflows/         # CI/CD pipelines
```

## Installation

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Azure subscription (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/cezcub/debate-coachr.git
   cd debate-coachr
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will be available at `http://localhost:8501`

## Usage

### Case Analysis

1. Navigate to the "Case Analysis" tab
2. Enter the debate resolution
3. Select your side (Pro/Con)
4. Choose upload format:
   - **Plaintext**: For standard case analysis
   - **Card Format**: For structured debate cards (extracts bolded/highlighted text)
5. Upload your file (TXT, DOCX, or PDF)
6. Receive detailed AI feedback

### Transcription Analysis

1. Navigate to the "PF Feedback" tab
2. Enter the debate resolution
3. Select your side (Pro/Con)
4. Upload or paste your round transcription
5. Get comprehensive feedback on performance and strategy

## File Format Support

- **TXT**: Plain text files
- **DOCX**: Microsoft Word documents (supports formatting detection for card format)
- **PDF**: Portable Document Format (limited formatting detection)

### Card Format Processing

When using "Card Format" mode:
- **DOCX**: Extracts bolded and highlighted text for focused analysis
- **PDF**: Basic text extraction with formatting limitations
- **TXT**: Treats as plain text

## Deployment

### Azure Container Apps

The application is configured for deployment to Azure Container Apps with:
- Managed identity authentication
- Azure Container Registry integration
- OIDC authentication for GitHub Actions
- Automatic scaling and high availability

See the [deployment documentation](docs/DEPLOYMENT_STRATEGY.md) for detailed setup instructions.

### Environment Variables

Required environment variables:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL

## API Endpoints

### Case Analysis
- `POST /process_text`: Analyze debate case text
- Parameters: `resolution`, `side`, `upload_format`, `file`

### Transcription Analysis  
- `POST /pf_feedback`: Analyze debate round transcription
- Parameters: `resolution`, `side`, `transcription`

## Development

### Running Tests
```bash
python -m pytest unit_tests/
```

### Docker Development
```bash
docker-compose -f deployment/docker/docker-compose.yml up
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **"Azure OpenAI credentials not found"**
   - Ensure `.env` file exists with correct API key and endpoint
   - Check environment variable names match exactly

2. **"Expecting value: line 1 column 1 (char 0)"**
   - Usually indicates Azure OpenAI model deployment issues
   - Verify your model deployment name matches the code
   - Check Azure OpenAI endpoint accessibility

3. **File processing errors**
   - Ensure required packages are installed (`python-docx`, `PyPDF2`)
   - Check file format compatibility
   - Verify file is not corrupted

### Debug Mode

Enable debug output by checking the console logs in your browser developer tools or terminal output.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the [documentation](docs/) for detailed guides
- Review troubleshooting section above

## Acknowledgments

- Built for high school public forum debate communities
- Powered by Azure OpenAI GPT-4
- Inspired by the need for accessible debate coaching tools
