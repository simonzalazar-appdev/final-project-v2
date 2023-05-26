namespace :slurp do
  desc "TODO"
  task teams: :environment do
    require "csv"

    csv_text = File.read(Rails.root.join("lib", "csvs", "clubs.csv"))
    csv = CSV.parse(csv_text, :headers => true, :encoding => "ISO-8859-1")

    csv.each do |row|
      club = Team.new
      club.club_name = row["club_name"]
      club.club_league = row["league_name"]
      club.league_id = row["league_id"]
      club.club_id2 = row["id"]
      club.save
      puts "#{club.club_name} saved"
    end

    puts "There are now #{Team.count} rows in the clubs table"
  end

  task vars: :environment do
    require "csv"

    csv_text = File.read(Rails.root.join("lib", "csvs", "vars.csv"))
    csv = CSV.parse(csv_text, :headers => true, :encoding => "ISO-8859-1")

    csv.each do |row|
      var = PlayerVar.new
      var.var = row["var"]
      var.desc = row["description"]
      var.save
      puts "#{var.desc} saved"
    end

    puts "There are now #{PlayerVar.count} rows in the clubs table"
  end

  task seasons: :environment do
    require "csv"

    csv_text = File.read(Rails.root.join("lib", "csvs", "seasons.csv"))
    csv = CSV.parse(csv_text, :headers => true, :encoding => "ISO-8859-1")

    csv.each do |row|
      s1 = Season.new
      s1.season = row['season']
      s1.save
      puts "#{s1.season} saved"
    end

    puts "There are now #{Season.count} rows in the seasons table"
  end

  task remove_all: :environment do
    Season.destroy_all
    PlayerVar.destroy_all
  end

end
