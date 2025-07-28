@home_bp.route('/')
@home_bp.route('/home')
def homepage():
    return render_template('home.html')

