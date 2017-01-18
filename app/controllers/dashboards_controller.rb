class DashboardsController < ApplicationController

  def index
    @topoType = TopoType.type
  end

  def create
    topo_type = params[:opts][:topo_type]
    opts = params[:opts].except(:topo_type).to_unsafe_h
    # print opts
    render json: TopoType.create_network(topo_type, opts).merge({:type => topo_type})
  end
end
