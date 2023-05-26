class TeamsController < ApplicationController
  def index
    matching_teams = Team.all

    @list_of_teams = matching_teams.order({ :created_at => :desc })

    render({ :template => "teams/index.html.erb" })
  end

  def show
    the_id = params.fetch("path_id")

    matching_teams = Team.where({ :id => the_id })

    @the_team = matching_teams.at(0)

    render({ :template => "teams/show.html.erb" })
  end

  def create
    the_team = Team.new
    the_team.club_league = params.fetch("query_club_league")
    the_team.club_name = params.fetch("query_club_name")
    the_team.league_id = params.fetch("query_league_id")
    the_team.club_id2 = params.fetch("query_club_id2")

    if the_team.valid?
      the_team.save
      redirect_to("/teams", { :notice => "Team created successfully." })
    else
      redirect_to("/teams", { :alert => the_team.errors.full_messages.to_sentence })
    end
  end

  def update
    the_id = params.fetch("path_id")
    the_team = Team.where({ :id => the_id }).at(0)

    the_team.club_league = params.fetch("query_club_league")
    the_team.club_name = params.fetch("query_club_name")
    the_team.league_id = params.fetch("query_league_id")
    the_team.club_id2 = params.fetch("query_club_id2")

    if the_team.valid?
      the_team.save
      redirect_to("/teams/#{the_team.id}", { :notice => "Team updated successfully."} )
    else
      redirect_to("/teams/#{the_team.id}", { :alert => the_team.errors.full_messages.to_sentence })
    end
  end

  def destroy
    the_id = params.fetch("path_id")
    the_team = Team.where({ :id => the_id }).at(0)

    the_team.destroy

    redirect_to("/teams", { :notice => "Team deleted successfully."} )
  end
end
