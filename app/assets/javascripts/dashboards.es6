//= require vue/dist/vue
//= require vue-lazyload/vue-lazyload
//= require axios/dist/axios
//= require ./sigma.min.js
//= require ./sigma_setting.js

new Vue({
  el: "#container",

  mounted() {
    const self = this
  },

  data() {
    return {
      opts: {
        topoType: "SW_2D",
        networkSize: 64,
        xSize: 8,
        baseType: "torus",
        randomLinkType: "fixed",
        nRandomLink: 2,
        alphaValues: [1.6, 1.6],
        boundedDegree: true,
      },

      showCustomizeAlpha: false,
      showResultPanel: false,
      viewLink: 0,

      geos: [],
      edges: [],
      nRandomLink: 0,
      diameter: 0,
      averageRandomLinkLength: 0,

      sigma: null,
      graph: {},
    }
  },

  watch: {
    'viewLink': function() {
      this.showRandomLink()
    },
  },

  methods: {
    requestCreate() {
      this.$set(this, "showResultPanel", false)
      return axios.post(`/dashboards/create`, {
        "opts" : {
          "topo_type" : this.opts.topoType,
          "network_size" : this.opts.networkSize,
          "x_size" : this.opts.xSize,
          "base_type" : this.opts.baseType,
          "random_link_type" : this.opts.randomLinkType,
          "n_random_link" : this.opts.nRandomLink,
          "random_link_type" : this.opts.randomLinkType,
          "is_bounded" : this.opts.boundedDegree,
          "alphas" : this.opts.alphaValues,
        }
      }).then((res) => {
        const data = res.data
        this.$set(this, "geos", data.geos)
        this.$set(this, "edges", data.edges)
        this.$set(this, "nRandomLink", data.n_random_links)
        this.$set(this, "diameter", data.diameter)
        this.$set(this, "averageRandomLinkLength", data.average_random_link_length)

        this.$set(this, "graph", this.createGraph(this.geos, this.edges))

        if (this.sigma) this.clear(this.sigma)
        this.$set(this, "sigma", this.newGraph(this.graph, sigmaSettings))
        
        this.$set(this, "showResultPanel", true)
      }, (err) => {

      })
    },

    clear(sigma) {
      if (sigma.graph.nodes().length > 0) sigma.kill();
    },

    showRandomLink() {
      var s = this.sigma
      this.clear(s)
      s = this.newGraph(this.graph, sigmaSettings)

      const tmpViewLink = this.viewLink
      if (this.viewLink > 0) {
        s.graph.edges().forEach(function(edge) {
          if (edge.nAlpha && edge.nAlpha == tmpViewLink) {
            // edge.color = COLORS[e.value];
          } else {
            s.graph.dropEdge(edge.id)
          }
        })
      }
      s.refresh()

      this.$set(this, "sigma", s)
    },

    createGraph(geos, edges) {
      const nNode = geos.length;
      const nEdge = edges.length;

      var isNeighbor = (x, y) => {
        if (!geos[x] || !geos[y]) return true;
        return Math.abs(geos[x][1] - geos[y][1]) + Math.abs(geos[x][2] - geos[y][2]) == 1;
      }

      var graph = {
        nodes: [],
        edges: []
      };

      var xSpace = 70,
          ySpace = 50;
      for (let i = 0; i < nNode; i++) {
        graph.nodes.push({
          id: 'n' + geos[i][0],
          label: 'n' + geos[i][0],
          x: geos[i][1] * xSpace,
          y: geos[i][2] * ySpace,
          size: 1,
          color: '#666'
        });
      }

      for (let i = 0; i < nEdge; i++) {
        const x = edges[i][0],
              y = edges[i][1];
        if (x >= nNode || y >= nNode) continue;
        
        var type = (isNeighbor(edges[i][0], edges[i][1])) ? 'line' : 'curve',
            isRandom = false,
            color = '#ccc';
        if (edges[i][2] >= 0) isRandom = true;
        if (edges[i][2]) color = COLORS[edges[i][2]];

        graph.edges.push({
          id: 'e' + i,
          label: 'e' + edges[i][0] + ':' + edges[i][1],
          source: 'n' + edges[i][0],
          target: 'n' + edges[i][1],
          color: color,
          size: 2,
          hover_color: '#000',
          type: type,
          is_random: isRandom,
          nAlpha: Number(edges[i][2]),
          alpha: edges[i][3]
        })
      }
      return graph
    },

    newGraph(graph, settings) {
      return new sigma({
        graph: graph,
        renderer: {
          container: 'network-container',
          type: 'canvas'
        },
        settings: settings
      });
    }
  },
})
