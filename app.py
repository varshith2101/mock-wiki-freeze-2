from os import path
from pathlib import Path
from flask import Flask, render_template
from flask_frozen import Freezer

# Define the templates folder path
template_folder = path.abspath('./wiki')

# Initialize Flask app
app = Flask(__name__, template_folder=template_folder)

# Flask-Frozen configuration
app.config['FREEZER_DESTINATION'] = 'public'  # Output folder for frozen site
app.config['FREEZER_RELATIVE_URLS'] = True    # Use relative URLs
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
freezer = Freezer(app)

# CLI command to freeze the site
@app.cli.command()
def freeze():
    """Generate a static version of the site."""
    freezer.freeze()

# CLI command to serve the frozen site locally
@app.cli.command()
def serve():
    """Serve the frozen site locally for testing."""
    freezer.run()

# Routes
@app.route('/')
def home():
    """Route for the homepage."""
    return render_template('pages/home.html')

@app.route('/<page>')
def pages(page):
    """
    Route for dynamic pages.
    Renders templates from 'wiki/pages/' based on the provided page name.
    """
    try:
        # Construct the path dynamically and render the template
        return render_template(f'pages/{page.lower()}.html')
    except Exception as e:
        # Return a 404 page or error message
        return f"Page not found: {str(e)}", 404

# Main function, runs at http://0.0.0.0:8080
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
