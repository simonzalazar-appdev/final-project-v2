class PlayerVarsController < ApplicationController
  def index
    matching_player_vars = PlayerVar.all

    @list_of_player_vars = matching_player_vars.order({ :created_at => :desc })

    render({ :template => "player_vars/index.html.erb" })
  end

  def show
    the_id = params.fetch("path_id")

    matching_player_vars = PlayerVar.where({ :id => the_id })

    @the_player_var = matching_player_vars.at(0)

    render({ :template => "player_vars/show.html.erb" })
  end

  def create
    the_player_var = PlayerVar.new
    the_player_var.var = params.fetch("query_var")
    the_player_var.desc = params.fetch("query_desc")

    if the_player_var.valid?
      the_player_var.save
      redirect_to("/player_vars", { :notice => "Player var created successfully." })
    else
      redirect_to("/player_vars", { :alert => the_player_var.errors.full_messages.to_sentence })
    end
  end

  def update
    the_id = params.fetch("path_id")
    the_player_var = PlayerVar.where({ :id => the_id }).at(0)

    the_player_var.var = params.fetch("query_var")
    the_player_var.desc = params.fetch("query_desc")

    if the_player_var.valid?
      the_player_var.save
      redirect_to("/player_vars/#{the_player_var.id}", { :notice => "Player var updated successfully."} )
    else
      redirect_to("/player_vars/#{the_player_var.id}", { :alert => the_player_var.errors.full_messages.to_sentence })
    end
  end

  def destroy
    the_id = params.fetch("path_id")
    the_player_var = PlayerVar.where({ :id => the_id }).at(0)

    the_player_var.destroy

    redirect_to("/player_vars", { :notice => "Player var deleted successfully."} )
  end
end
