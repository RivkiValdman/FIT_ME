from data.database import Database

class MakeupService:
	def __init__(self, db):
		self.db = db

	def match_makeup(self, user):
		return self.db.find_makeup_for_skin_tone(user.skin_tone)