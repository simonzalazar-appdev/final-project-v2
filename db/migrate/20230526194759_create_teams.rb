class CreateTeams < ActiveRecord::Migration[6.0]
  def change
    create_table :teams do |t|
      t.string :club_league
      t.string :club_name
      t.integer :league_id
      t.integer :club_id2

      t.timestamps
    end
  end
end
