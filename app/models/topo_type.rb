class TopoType < ApplicationRecord
  TOPO_NAME = {
    :sw_torus2d => "SW_TORUS2D",
    :torus2d => "TORUS2D",
    :jellyfish => "JELLYFISH"
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
    result = %x[ python #{GENERATOR_DIR}/sw-2DTorus.py #{size} #{x_size} #{alphas} ]
    
    files = result.split("\n").last(2)
    file_edges = "#{RESULT_DIR}/network_generator/results/sw_2DTorus_n#{size}xSize#{x_size}_r#{n_random_links}.edges"
    file_geo = "#{RESULT_DIR}/network_generator/results/sw_2DTorus_n#{size}xSize#{x_size}_r#{n_random_links}.geos"

    geo = []
    File.foreach(file_geo) do |line|
      geo << line.split(" ")
    end
    
    edges = []
    File.foreach(file_edges) do |line|
      edges << line.split(" ")
    end

    # print edges
    # print opts[:alphas]
    (0...n_random_links).each do |i|
      f = "#{RESULT_DIR}/network_generator/results/listr#{i}"
      File.foreach(f) do |line|
        tmp = line.split(" ")

        # print tmp
        # print i
        # print opts[:probs].values[i]
        ii = edges.index(tmp)
        if ii
          edges[ii][2] = i
          edges[ii][3] = opts[:alphas].values[i]
        end
      end      
    end

    {
      geo: geo,
      edges: edges,
      n_random_links: n_random_links
    }
  end

end
