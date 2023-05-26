Rails.application.routes.draw do
  # Routes for the Team resource:

  # CREATE
  post("/insert_team", { :controller => "teams", :action => "create" })
          
  # READ
  get("/teams", { :controller => "teams", :action => "index" })
  
  get("/teams/:path_id", { :controller => "teams", :action => "show" })
  
  # UPDATE
  
  post("/modify_team/:path_id", { :controller => "teams", :action => "update" })
  
  # DELETE
  get("/delete_team/:path_id", { :controller => "teams", :action => "destroy" })

  #------------------------------

  #routes for model
  post("/insert_model", { :controller => "model", :action => "create_model" })


  # Routes for the Player var resource:

  # CREATE
  post("/insert_player_var", { :controller => "player_vars", :action => "create" })
          
  # READ
  get("/player_vars", { :controller => "player_vars", :action => "index" })
  
  get("/player_vars/:path_id", { :controller => "player_vars", :action => "show" })
  
  # UPDATE
  
  post("/modify_player_var/:path_id", { :controller => "player_vars", :action => "update" })
  
  # DELETE
  get("/delete_player_var/:path_id", { :controller => "player_vars", :action => "destroy" })

  #------------------------------

  # Routes for the Season resource:

  # CREATE
  post("/insert_season", { :controller => "seasons", :action => "create" })
          
  # READ
  get("/seasons", { :controller => "seasons", :action => "index" })
  
  get("/seasons/:path_id", { :controller => "seasons", :action => "show" })
  
  # UPDATE
  
  post("/modify_season/:path_id", { :controller => "seasons", :action => "update" })
  
  # DELETE
  get("/delete_season/:path_id", { :controller => "seasons", :action => "destroy" })

  #------------------------------

  # Routes for the Club resource:

  # CREATE
  post("/insert_club", { :controller => "clubs", :action => "create" })
          
  # READ
  get("/clubs", { :controller => "clubs", :action => "index" })
  
  get("/clubs/:path_id", { :controller => "clubs", :action => "show" })
  
  # UPDATE
  
  post("/modify_club/:path_id", { :controller => "clubs", :action => "update" })
  
  # DELETE
  get("/delete_club/:path_id", { :controller => "clubs", :action => "destroy" })

  #------------------------------

  get("/", { :controller => "application", :action => "index" })
  # Routes for the Bookmark resource:

  # CREATE
  post("/insert_bookmark", { :controller => "bookmarks", :action => "create" })
          
  # READ
  get("/bookmarks", { :controller => "bookmarks", :action => "index" })
  
  get("/bookmarks/:path_id", { :controller => "bookmarks", :action => "show" })
  
  # UPDATE
  
  post("/modify_bookmark/:path_id", { :controller => "bookmarks", :action => "update" })
  
  # DELETE
  get("/delete_bookmark/:path_id", { :controller => "bookmarks", :action => "destroy" })

  #------------------------------

  # Routes for the User account:

  # SIGN UP FORM
  get("/user_sign_up", { :controller => "user_authentication", :action => "sign_up_form" })        
  # CREATE RECORD
  post("/insert_user", { :controller => "user_authentication", :action => "create"  })
      
  # EDIT PROFILE FORM        
  get("/edit_user_profile", { :controller => "user_authentication", :action => "edit_profile_form" })       
  # UPDATE RECORD
  post("/modify_user", { :controller => "user_authentication", :action => "update" })
  
  # DELETE RECORD
  get("/cancel_user_account", { :controller => "user_authentication", :action => "destroy" })

  # ------------------------------

  # SIGN IN FORM
  get("/user_sign_in", { :controller => "user_authentication", :action => "sign_in_form" })
  # AUTHENTICATE AND STORE COOKIE
  post("/user_verify_credentials", { :controller => "user_authentication", :action => "create_cookie" })
  
  # SIGN OUT        
  get("/user_sign_out", { :controller => "user_authentication", :action => "destroy_cookies" })
             
  #------------------------------

  # Routes for the Character resource:

  # CREATE
  post("/insert_character", { :controller => "characters", :action => "create" })
          
  # READ
  get("/characters", { :controller => "characters", :action => "index" })
  
  get("/characters/:path_id", { :controller => "characters", :action => "show" })
  
  # UPDATE
  
  post("/modify_character/:path_id", { :controller => "characters", :action => "update" })
  
  # DELETE
  get("/delete_character/:path_id", { :controller => "characters", :action => "destroy" })

  #------------------------------

  # Routes for the Movie resource:

  # CREATE
  post("/insert_movie", { :controller => "movies", :action => "create" })
          
  # READ
  get("/movies", { :controller => "movies", :action => "index" })
  
  get("/movies/:path_id", { :controller => "movies", :action => "show" })
  
  # UPDATE
  
  post("/modify_movie/:path_id", { :controller => "movies", :action => "update" })
  
  # DELETE
  get("/delete_movie/:path_id", { :controller => "movies", :action => "destroy" })

  #------------------------------

  # Routes for the Director resource:

  # CREATE
  post("/insert_director", { :controller => "directors", :action => "create" })
          
  # READ
  get("/directors", { :controller => "directors", :action => "index" })
  
  get("/directors/:path_id", { :controller => "directors", :action => "show" })
  
  # UPDATE
  
  post("/modify_director/:path_id", { :controller => "directors", :action => "update" })
  
  # DELETE
  get("/delete_director/:path_id", { :controller => "directors", :action => "destroy" })

  #------------------------------

  # Routes for the Actor resource:

  # CREATE
  post("/insert_actor", { :controller => "actors", :action => "create" })
          
  # READ
  get("/actors", { :controller => "actors", :action => "index" })
  
  get("/actors/:path_id", { :controller => "actors", :action => "show" })
  
  # UPDATE
  
  post("/modify_actor/:path_id", { :controller => "actors", :action => "update" })
  
  # DELETE
  get("/delete_actor/:path_id", { :controller => "actors", :action => "destroy" })

  #------------------------------

end
