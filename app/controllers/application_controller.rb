class ApplicationController < ActionController::Base
  def index_old

    player_vars = `python3 -c 'import python_ruby_bridge as prb; print(prb.return_vars())'`
    @player_vars = player_vars[1..-1].split(",")
    clubs = `python3 -c 'import python_ruby_bridge as prb; print(prb.return_clubs2())'`
    @clubs = clubs[1..-1].split(",")
    render({ :template => "index.html.erb" })
  end

  def index
    @clubs = Team.all
    @player_vars = PlayerVar.all
    @seasons = Season.all

    #@list_of_movies = matching_movies.order({ :created_at => :desc })

    render({ :template => "index.html.erb" })
  end

end
