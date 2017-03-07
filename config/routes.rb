Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  # resources :dashboards

  get '/dashboards', to: 'dashboards#index'
  post '/dashboards/create', to: 'dashboards#create'
  post '/dashboards/upload', to: 'dashboards#upload'
  get '/test', to: 'dashboards#show' 
end
