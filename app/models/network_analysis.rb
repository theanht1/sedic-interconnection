class NetworkAnalysis
  def self.network_analysis file_geos, file_edges
    result = %x[ python #{TopoType::GENERATOR_DIR}/network_analysis.py #{file_geos} #{file_edges} ]
    eval(result) rescue nil
  end
end
