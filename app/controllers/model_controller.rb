class ModelController < ActionController::Base
  def create_model
    require "csv"

    hash_data = params
    home_team_id = params.fetch(:team_home)
    @home_team = Team.where({ :club_id2 => home_team_id }).at(0).club_name
    away_team_id = params.fetch(:team_away)
    @away_team = Team.where({ :club_id2 => away_team_id }).at(0).club_name

    csv_file_path = "selected_params.csv"

    CSV.open(csv_file_path, "w") do |csv|
      csv << hash_data.keys
      csv << hash_data.values
    end

    puts "CSV saved to #{csv_file_path}"

    results = `python3 -c 'import main as main; print(main.predict_match())'`
    results = results[1..4].split(",")
    @score_home = results[0]
    @score_away = results[1]
    render({ :template => "test.html.erb" })
  end
end
