# == Schema Information
#
# Table name: teams
#
#  id          :integer          not null, primary key
#  club_id2    :integer
#  club_league :string
#  club_name   :string
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#  league_id   :integer
#
class Team < ApplicationRecord
end
