# LinkMaster Network Link Management System

A Django-based web application for managing and analyzing network microwave links. This system provides tools for uploading, searching, and visualizing network link data, with features for cascade analysis and site connectivity mapping.

## Screenshot


![Screenshot of the SF6 Network Link Management System](docs/images/screenshot.png)

## Features

- Excel file upload for bulk link data import
- Real-time progress tracking for data processing
- Link search functionality by site ID
- Site connectivity visualization
- Cascade analysis for network impact assessment
- Export functionality for affected sites

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YahiaG/LinkMaster.git
cd LinkMaster
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv link_env
link_env\Scripts\activate

# Linux/Mac
python3 -m venv link_env
source link_env/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

1. **Upload Link Data**

   - Navigate to the upload page
   - Select an Excel file containing link data
   - The system will process the file and show real-time progress

2. **Search Links**

   - Use the search functionality to find links by site ID
   - View detailed information about specific links

3. **View Connectivity**
   - Access the connectivity page to visualize site relationships
   - Generate cascade analysis for network impact assessment

## Project Structure

- `links/` - Main application directory
  - `views.py` - Contains all view functions
  - `models.py` - Database models
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JavaScript)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Yahia ElGamily - Yahia.ElGamily@gmail.com

Project Link: [https://github.com/YahiaG/LinkMaster](https://github.com/YahiaG/LinkMaster)
