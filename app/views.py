from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from app.models import Movies, ArticlesSchema
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()}) 


@app.route('/api/v1/movies', methods=['GET'])
def movies():
    movies = Movies.query.all()
    result = []
    for movie in movies:
        result.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": movie.poster
        })
    return jsonify(result)


@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)






from werkzeug.datastructures import CombinedMultiDict

@app.route('/api/v1/movies', methods=['POST'])
def add_movie():
    try:
        form = MovieForm(CombinedMultiDict([request.form, request.files]))

        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            poster = form.poster.data

            filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            movie = Movies(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                "message": "Movie Successfully added",
                "title": movie.title,
                "poster": movie.poster,
                "description": movie.description
            }), 201

        return jsonify({'errors': form_errors(form)}), 400
    
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

###
# The functions below should be applicable to all Flask apps.
###

# Collect form errors from Flask-WTF
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)
    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404