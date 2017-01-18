class TopoType < ApplicationRecord
  TOPO_NAME = {
    :sw_torus2d => "SW_TORUS2D",
    :torus2d => "TORUS2D",
    :jellyfish => "JELLYFISH"
  }

  GENERATOR_DIR = File.expand_path("../../network_generator", __dir__)

  def self.type
    TOPO_NAME.values
  end

  def self.create_network type_name, size
    topo_type = TOPO_NAME.key(type_name.to_s)
    self.send("create_" + topo_type.to_s, size)
  end

  def self.create_sw_torus2d size
    p GENERATOR_DIR
    result = %x[ python2 #{GENERATOR_DIR}/sw-2DTorus0.2.py #{size} 2 ]
    p result
  end

end
