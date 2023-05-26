class ClubsController < ApplicationController
  def index
    matching_clubs = Club.all

    @list_of_clubs = matching_clubs.order({ :created_at => :desc })

    render({ :template => "clubs/index.html.erb" })
  end

  def show
    the_id = params.fetch("path_id")

    matching_clubs = Club.where({ :id => the_id })

    @the_club = matching_clubs.at(0)

    render({ :template => "clubs/show.html.erb" })
  end

  def create
    the_club = Club.new
    the_club.club_leagu2e = params.fetch("query_club_leagu2e")
    the_club.club_name = params.fetch("query_club_name")
    the_club.league_id = params.fetch("query_league_id")
    the_club.club_id2 = params.fetch("query_club_id2")

    if the_club.valid?
      the_club.save
      redirect_to("/clubs", { :notice => "Club created successfully." })
    else
      redirect_to("/clubs", { :alert => the_club.errors.full_messages.to_sentence })
    end
  end

  def update
    the_id = params.fetch("path_id")
    the_club = Club.where({ :id => the_id }).at(0)

    the_club.club_leagu2e = params.fetch("query_club_leagu2e")
    the_club.club_name = params.fetch("query_club_name")
    the_club.league_id = params.fetch("query_league_id")
    the_club.club_id2 = params.fetch("query_club_id2")

    if the_club.valid?
      the_club.save
      redirect_to("/clubs/#{the_club.id}", { :notice => "Club updated successfully."} )
    else
      redirect_to("/clubs/#{the_club.id}", { :alert => the_club.errors.full_messages.to_sentence })
    end
  end

  def destroy
    the_id = params.fetch("path_id")
    the_club = Club.where({ :id => the_id }).at(0)

    the_club.destroy

    redirect_to("/clubs", { :notice => "Club deleted successfully."} )
  end
end
