from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import sys, json
sys.path.append("/home/wleong/Personal_project/StockTracker/")
from models.model import Model
from processing.data_processing import DataProcessing
from src.live_price_display import LivePriceDisplay
from src.news_display import NewsDisplay
import pandas as pd

# Create your views here.
models = Model()
dp = DataProcessing()
news_disp = NewsDisplay()
price_disp = LivePriceDisplay()

def index(request):
    options = models.company_list
    return render(request, 'dashboard.html', {'dropdown_items': options}) 
    
def update_graph(request):
    company = request.GET.get('company')
    raw_data = dp.data[company]
    data = {
        "date": raw_data["date"],
        "close": raw_data["close"]
    }
    df = pd.DataFrame(data)
    chart_data = df.to_json(orient='records')
    return JsonResponse(chart_data, safe=False)

def update_price(request):
    company = request.GET.get('company')
    price = price_disp.display_final_price_yf(company)
    return HttpResponse(price)

def update_news(request):
    company = request.GET.get('company')
    news = json.dumps(news_disp.collect_news(company))
    return HttpResponse(news)