class NetworkAnalysis
  def self.network_analysis file_geos, file_edges, file_stats = nil
    result = %x[ python3 #{TopoType::GENERATOR_DIR}/network_analysis.py #{file_geos} #{file_edges} ]
    result = eval(result) rescue nil

    average_random_link_path = []
    if file_stats.present?
      File.open(file_stats, "r").each do |line|
        average_random_link_path << line.to_f
      end
    end

    result.merge({
      "average_random_link_length" => average_random_link_path,
    })
  end
end
