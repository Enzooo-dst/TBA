class Item:
  def __init__(self, name):
      self.name = name    #nom de l'objet
      self.description = "" #descripiton de l'objet
      self.weight = 0  # Poids de l'objet
      self.inventory = {}
  def __str__(self):
          return f"{self.name} : {self.description} ({self.weight} kg)"
