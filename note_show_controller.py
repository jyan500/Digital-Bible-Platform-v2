from config import mysql
from extensions import *

note_show_controller = Blueprint('note_show_controller', __name__)
@note_show_controller.route('/note_show_controller', methods = ["GET", "POST"])
def note_show_page():
	return render_template('notes.html')

