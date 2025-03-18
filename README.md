# MaLDReTH - Research Data Lifecycle Visualization

This Streamlit application visualizes the MaLDReTH (Mapping the Landscape of Digital Research Tools Harmonised) framework, developed by the Research Data Alliance to help researchers, data managers, and tool developers navigate the complex ecosystem of digital tools used throughout the research data lifecycle.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/yourusername/maldreth-streamlit/main/streamlit_app.py)

## Features

- Interactive visualization of the Research Data Lifecycle
- Browsing of tool categories and examples for each lifecycle stage
- Searching for specific tools across the lifecycle
- Responsive design for desktop and mobile devices

## Technologies

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **SQLite**: Database for storing tool information
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation

## Project Structure

```
maldreth-streamlit/
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── resources/
│   ├── schema.sql          # Database schema
│   ├── tools.csv           # Tool data (if available)
│   └── maldreth-logo.svg   # Logo file
├── streamlit_app.py        # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Getting Started

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/maldreth-streamlit.git
   cd maldreth-streamlit
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```

5. Open your browser and go to `http://localhost:8501`

### Deployment

This application is designed to be deployed on Streamlit Cloud, which provides free hosting for Streamlit applications linked to public GitHub repositories.

1. Push your code to a public GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account
3. Deploy the application by linking it to your repository and the `streamlit_app.py` file
4. Wait for the deployment to complete and access your application via the provided URL

## Research Data Lifecycle

The research data lifecycle consists of 12 interconnected stages, each representing a critical phase in the research process:

1. **Conceptualise**: Formulating research ideas and defining data requirements
2. **Plan**: Creating structured frameworks for research project management
3. **Fund**: Acquiring financial resources to support the research project
4. **Collect**: Gathering reliable, high-quality data
5. **Process**: Preparing data for analysis through cleaning and structuring
6. **Analyse**: Deriving insights and knowledge from processed data
7. **Store**: Securely recording data while maintaining integrity
8. **Publish**: Making research data available with appropriate metadata
9. **Preserve**: Ensuring long-term data safety and accessibility
10. **Share**: Making data available to humans and machines
11. **Access**: Controlling and managing data access
12. **Transform**: Creating new data from original sources

## Tool Categories

For each stage of the research data lifecycle, the application provides:

- Categories of tools relevant to that stage
- Descriptions of what each category of tools does
- Example tools within each category

## Contributing

We welcome contributions to improve the MaLDReTH visualization tool! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Acknowledgments

- Research Data Alliance (RDA) and Oracle for Research "Mapping the Landscape of Digital Research Tools" Working Group
- All contributors to the MaLDReTH framework
