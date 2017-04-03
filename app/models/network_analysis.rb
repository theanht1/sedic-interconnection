class NetworkAnalysis
  def self.network_analysis file_geos, file_edges, file_stats
    result = %x[ python3 #{TopoType::GENERATOR_DIR}/network_analysis.py #{file_geos} #{file_edges} ]
    result = eval(result) rescue nil

    average_random_link_path = []
    File.open(file_stats, "r").each do |line|
      average_random_link_path << line.to_f
    end

    result.merge({
      "average_random_link_path" => average_random_link_path,
    })
  end
end
