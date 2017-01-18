class DashboardsController < ApplicationController

  def index
    @topoType = TopoType.type
  end

  def create
    render json: TopoType.create_network(params[:topo_type], params[:network_size])
  end
end
