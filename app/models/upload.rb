class Upload < ApplicationRecord
  def self.create_network_from_file geos_string, edges_string
    geos_array = geos_string.split("\n")
    edges_array = edges_string.split("\n")

    n = geos_array.first.to_i
    geos = []
    (1..n).each do |i| 
      geos << geos_array[i].split(" ").map(&:to_i) if geos_array[i].present?
    end
    
    edges = []
    n, n_link, n_random_links = edges_array.first.split(' ').map(&:to_i)

    (1..n_link).each do |i|
      edges << edges_array[i].split(' ').map(&:to_i) if edges_array[i].present?
    end    

    {
      geos: geos,
      edges: edges,
      n_random_links: n_random_links
    }
  end
end
