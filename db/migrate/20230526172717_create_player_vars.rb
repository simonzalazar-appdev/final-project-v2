class CreatePlayerVars < ActiveRecord::Migration[6.0]
  def change
    create_table :player_vars do |t|
      t.string :var
      t.string :desc

      t.timestamps
    end
  end
end
