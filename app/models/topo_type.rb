class TopoType < ApplicationRecord
  TOPO_NAME = {
    :sw_torus2d => "SW_TORUS2D",
    :sw_grid2d => "SW_GRID2D"
  }

  GENERATOR_DIR = File.expand_path("../../network_generator", __dir__)
  RESULT_DIR = File.expand_path("../../", __dir__)

  def self.type
    TOPO_NAME.values
  end

  def self.create_network type_name, opts = {}
    topo_type = TOPO_NAME.key(type_name.to_s)
    self.send("create_" + topo_type.to_s, opts)
  end

  def self.create_sw_torus2d opts
    # print opts.to_h
    size = opts[:network_size]
    n_random_links = opts[:n_random_links].to_i
    x_size = opts[:x_size]
    alphas = opts[:alphas].values.join(" ")
    result = %x[ python #{GENERATOR_DIR}/sw-2DTorus_Node_xSize_ri.py #{size} #{x_size} #{alphas} ]
    
    file_edges = "#{RESULT_DIR}/network_generator/results/sw_2DTorus_n#{size}xSize#{x_size}_r#{n_random_links}.edges"
    file_geos = "#{RESULT_DIR}/network_generator/results/sw_2DTorus_n#{size}xSize#{x_size}_r#{n_random_links}.geos"

    NetworkAnalysis.network_analysis(file_geos, file_edges)
  end

  def self.create_sw_grid2d opts
    # print opts.to_h
    size = opts[:network_size]
    n_random_links = opts[:n_random_links].to_i
    x_size = opts[:x_size]
    alphas = opts[:alphas].values.join(" ")
    result = %x[ python #{GENERATOR_DIR}/sw-2DGrid_Node_xSize_ri.py #{size} #{x_size} #{alphas} ]
    
    files = result.split("\n").last(2)
    file_edges = "#{RESULT_DIR}/network_generator/results/sw_2DGrid_n#{size}xSize#{x_size}_r#{n_random_links}.edges"
    file_geos = "#{RESULT_DIR}/network_generator/results/sw_2DGrid_n#{size}xSize#{x_size}_r#{n_random_links}.geos"
    
    NetworkAnalysis.network_analysis(file_geos, file_edges)
  end
end
