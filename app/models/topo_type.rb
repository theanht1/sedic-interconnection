class TopoType < ApplicationRecord
  TOPO_NAME = {
    :sw_torus2d => "SW_TORUS2D",
    :torus2d => "TORUS2D",
    :jellyfish => "JELLYFISH"
  }

  GENERATOR_DIR = File.expand_path("../../network_generator", __dir__)
  RESULT_DIR = File.expand_path("../../network_generator/results", __dir__)

  def self.type
    TOPO_NAME.values
  end

  def self.create_network type_name, size
    topo_type = TOPO_NAME.key(type_name.to_s)
    self.send("create_" + topo_type.to_s, size)
  end

  def self.create_sw_torus2d size    
    result = %x[ python2 #{GENERATOR_DIR}/sw-2DTorus0.2.py #{size} 2 ]
    file_edges = "#{RESULT_DIR}/sw_2DTorus0.2_n#{size}_r#{2}.edges"
    file_geo = "#{RESULT_DIR}/sw_2DTorus0.2_n#{size}_r#{2}.geo"

    geo = []
    File.foreach(file_geo) do |line|
      geo << line.split(" ")
    end
    
    edges = []
    File.foreach(file_edges) do |line|
      edges << line.split(" ")
    end

    {
      geo: geo,
      edges: edges
    }
  end

end
