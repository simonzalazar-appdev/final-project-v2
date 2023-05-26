require "csv"

csv_text = File.read(Rails.root.join("lib", "csvs", "clubs.csv"))
csv = CSV.parse(csv_text, :headers => true, :encoding => "ISO-8859-1")

csv.each do |row|
  club = Club.new
  t.club_name = row["club_name"]
  t.club_league = row["league_name"]
  t.league_id = row["league_id"]
  t.save
  puts "#{t.club_name} saved"
end

puts "There are now #{Club.count} rows in the clubs table"
