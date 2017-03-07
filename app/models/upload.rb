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
    n, n_based_link, n_random_links = edges_array.first.split(' ').map(&:to_i)

    (1..n_based_link).each do |i|
      edges << edges_array[i].split(' ').map(&:to_i) if edges_array[i].present?
    end

    i = n_based_link + 1
    (1..n_random_links).each do |index|
      n_links, alpha = edges_array[i].split(' ').map(&:to_f) if edges_array[i].present?
      n_links = n_links.to_i
      i += 1
      (1..n_links).each do |linkIndex|
        edges << (edges_array[i].split(' ').map(&:to_i) << index << alpha if edges_array[i].present?)
        i += 1
      end
    end

    {
      geos: geos,
      edges: edges,
      n_random_links: n_random_links
    }
  end
end
