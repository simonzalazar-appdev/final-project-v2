# == Schema Information
#
# Table name: player_vars
#
#  id         :integer          not null, primary key
#  desc       :string
#  var        :string
#  created_at :datetime         not null
#  updated_at :datetime         not null
#
class PlayerVar < ApplicationRecord
end
