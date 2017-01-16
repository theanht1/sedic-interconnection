class DashboardsController < ApplicationController

  def index
    @topoType = TopoType.TYPE
  end
end
