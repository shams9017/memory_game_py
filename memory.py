

import pygame, random, time


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.


      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
     
      self.frame_counter = 0
      self.images = []
      self.imgs_to_match = []
      self.cover_image = pygame.image.load('image0.bmp')
      self.counter = 0
      self.tile_match_counter = 0
      self.time_elapsed = 0

      for i in range(1, 9):
         self.images.append(pygame.image.load("image{0}.bmp".format(str(i))))
 
      self.images = self.images + self.images
      random.shuffle(self.images)
      
      width = self.cover_image.get_width()
      height = self.cover_image.get_height()
     
      self.board_size = 4
      self.board = []

      self.mouse_coords = (0,0)
      self.counter = 0
      self.img = []
      img_num = 0
      for row_index in range(0, self.board_size):
         row = []
         for col_index in range(0, self.board_size):
            x = ((col_index)*width) + 1
            y = ((row_index)*height) + 1      
            tile = Tile(self.surface,x,y,width,height,self.images[img_num], self.cover_image)
            img_num += 1
            row.append(tile)
         self.board.append(row)
      
      
   def play(self):
      # Play the game until the player presses the clos box.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()    
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
  
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.continue_game == True:
             coords = pygame.mouse.get_pos()
             self.mouse_coords = coords
          
   def draw(self):
      # Draw all game objects.
      self.counter = 0
      self.surface.fill(self.bg_color) # clear the display surface first
      for row in self.board:       
         for tile in row:          
            tile.draw_tile()       
      self.cover_tile()
      self.hide_unmatched()               
      self.expose_tile(self.mouse_coords) 
      self.score_display()    
      pygame.display.update() # make the updated surface appear on the display
   

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      for r in self.board:
         for tile in r:
            if tile.get_state() == 'exposed':
               #if tile.image not in self.imgs_to_match:
               self.imgs_to_match.append(tile)
  
      if len(self.imgs_to_match) == 2:
         if self.imgs_to_match[0].matches(self.imgs_to_match[1]):
            self.imgs_to_match[0].state = 'matched'
            self.imgs_to_match[1].state = 'matched'
      self.imgs_to_match = [] 
        
      self.frame_counter = self.frame_counter + 1

   def decide_continue(self):
      # Check and remember if the game should continue


       for r in self.board:
         for tile in r:
            if tile.state == 'matched':
               self.tile_match_counter += 1
               if self.tile_match_counter == len(self.images):
                  self.continue_game = False
       self.tile_match_counter = 0

   def expose_tile(self, mouse_coords):
      # Expose a tile when called by the Game class``

      for row in self.board:
         for tile in row:
            if tile.rect.collidepoint(mouse_coords):
               tile.expose() 

   def cover_tile(self):
      # Cover the tiles when game starts

      for row in self.board:
         for tile in row:    
            if tile.state != 'exposed' and tile.state != 'matched': # Initially every time is exposed and unmatched, so this will run
               tile.draw_cover_image()
   
   def hide_unmatched(self):
      # Hide any tile not matched

      for row in self.board:
         for tile in row:    
            if tile.state == 'exposed':
               self.counter += 1          
               if self.counter > 2:    
                  for row in self.board:
                     for tile in row:
                        if tile.state != 'matched': 
                           tile.draw_cover_image()

   def timer(self):
      loop_break = False
      current_time = time.time()
      future_time = current_time + .05
      while time.time() < future_time:
         loop_break = True

      if loop_break == True:
         return True
      
   def score_display(self):
      # Display the score
      score_color = pygame.Color('white')
      font_game = pygame.font.SysFont('', 50)

      score = font_game.render(str(self.frame_counter//60), True, score_color)
  
      self.surface.blit(score, (self.surface.get_width() - score.get_width(),0))           
                    
                     
class Tile:
   def __init__(self, surface, horizontal_position, vertical_position, width, height, image, cover_image):
      # Initialize a Tile.
      # Takes the attributes needed to draw a rectangle and also the two types of images

      self.rect = pygame.Rect(horizontal_position, vertical_position, width, height)  
      self.rect_surface = surface
      self.state = ''
      self.image = image
      self.cover = cover_image
      

   def draw_tile(self):
      # Draw a tile on the surface
      # - self is the Tile
      border_width = 5
      border_color = pygame.Color('red')  
      pygame.draw.rect(self.rect_surface, border_color, self.rect, border_width)
      self.draw_image()
      
    
   def draw_image(self):
      # draws the image of the tile on itself
      self.rect_surface.blit(self.image, self.rect)
      
      
   def draw_cover_image(self):
      # draws the cover image for the tile itself
      self.rect_surface.blit(self.cover, self.rect)
      self.state = 'hidden'

   def expose(self):
      # Exposes the tile when called
      if self.state == 'hidden':          
         self.rect_surface.blit(self.image, self.rect)
         self.state = 'exposed'

   def get_state(self):
      # returns the state of a tile (matched, hidden, exposed or none)
      return self.state

   def matches(self, other_tile):
      # Checks if two tiles contain the same image
      # returns a boolean 
      if self.image == other_tile.image:
         return True

      
main()