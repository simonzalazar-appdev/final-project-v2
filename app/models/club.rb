# == Schema Information
#
# Table name: clubs
#
#  id          :integer          not null, primary key
#  club_league :string
#  club_name   :string
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#  league_id   :integer
#
class Club < ApplicationRecord
end
