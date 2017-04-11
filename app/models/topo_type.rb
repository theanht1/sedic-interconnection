class TopoType < ApplicationRecord
  TOPO_NAME = {
    :sw_2d => "SW_2D",
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

  def self.create_sw_2d opts
    # print opts.to_h
    size = opts[:network_size].to_i
    base_type = opts[:base_type]
    random_link_type = opts[:random_link_type]
    n_random_links = opts[:n_random_link].to_i
    is_bounded = opts[:is_bounded] || true

    x_size = opts[:x_size].to_i
    y_size = size / x_size
    size = x_size * y_size
    alphas = opts[:alphas].join(" ")

    Dir.chdir("network_generator/sedic-graph/src") {
      if random_link_type == "fixed"
        cmd_opts = "#{base_type} #{random_link_type} #{x_size} #{y_size} #{n_random_links} #{alphas}"
      else
        cmd_opts = "#{base_type} #{random_link_type} #{x_size} #{y_size} #{n_random_links} #{alphas} #{is_bounded}"
      end

      result = %x[ java smallworld.SmallWorld #{cmd_opts}]
      puts result

      file_name = "SW_2D_#{base_type}_#{random_link_type}_degree_#{size}_nodes_#{y_size}_cols_r#{n_random_links}"
      file_edges = "#{file_name}.edges"
      file_geos = "#{file_name}.geos"
      file_stats = "#{file_name}.stats"

      if size <= 20000
        NetworkAnalysis.network_analysis(file_geos, file_edges, file_stats)
      else
        {}
      end
    }

  end  
end
