from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Auction, Bid
from .forms import BidForm
from django.db.models import Max
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

class AuctionListView(ListView):
    model = Auction
    template_name = 'auctions.html'
    context_object_name = 'auction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auctions = context['object_list']

        for auction in auctions:
            cached_bid_keys = cache.keys(f'bid_{auction.id}_*')
            if cached_bid_keys:
                cached_bids = [cache.get(key) for key in cached_bid_keys if cache.get(key)]
                highest_bid = max(cached_bids)
            else:
                highest_bid = None

            cached_bid_str = cache.get(f'bid_{auction.id}_{self.request.user.id}')
            is_highest_bidder = cached_bid_str is not None and int(cached_bid_str) == highest_bid

            auction.highest_bid = highest_bid
            auction.is_highest_bidder = is_highest_bidder

        return context

class AuctionDetailView(DetailView):
    model = Auction
    template_name = 'auction_detail.html'
    context_object_name = 'auction'

    def post(self, request, *args, **kwargs):
        auction = self.get_object()
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            amount = bid_form.cleaned_data['amount']
            user_id = self.request.user.id
            cache_key = f'bid_{auction.id}_{user_id}'

            cached_bid_str = cache.get(cache_key)

            if cached_bid_str is None or int(cached_bid_str) < amount:
                remaining_time = auction.end_date - timezone.now()
                if remaining_time <= timezone.timedelta(minutes=15):
                    auction.end_date += timezone.timedelta(minutes=15)
                    auction.save()
                    messages.info(request, "Auction end time has been extended by 15 minutes.")
                cache.set(cache_key, amount, timeout=None)
                messages.success(request, "Your bid has been placed successfully.")
            else:
                messages.error(request, "You have already placed a higher bid on this auction.")

            return redirect('auctions')

        context = self.get_context_data(object=auction)
        context['bid_form'] = bid_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auction = self.object
        user_id = self.request.user.id

        cached_bid_keys = cache.keys(f'bid_{auction.id}_*')
        if cached_bid_keys:
            cached_bids = [cache.get(key) for key in cached_bid_keys if cache.get(key)]
            highest_bid = max(cached_bids)
        else:
            highest_bid = None

        cached_bid_str = cache.get(f'bid_{auction.id}_{user_id}')

        context['bid_form'] = BidForm(initial={'amount': highest_bid or auction.initial_price})
        context['highest_bid'] = highest_bid
        context['is_highest_bidder'] = cached_bid_str is not None and int(cached_bid_str) == highest_bid

        context['highest_general_bid'] = highest_bid

        return context

@login_required
def user_profile(request):
    user = request.user
    user_auctions = []

    for auction in Auction.objects.all():
        if auction.winner == user:
            user_auctions.append(auction)
        else:
            cached_bid_str = cache.get(f'bid_{auction.id}_{user.id}')
            if cached_bid_str is not None:
                cached_bid = int(cached_bid_str)
                cached_bids = [int(cache.get(key)) for key in cache.keys(f'bid_{auction.id}_*') if cache.get(key)]
                highest_bid = max(cached_bids) if cached_bids else None
                
                auction.highest_bid = highest_bid
                auction.highest_bidder = cached_bid == highest_bid
                user_auctions.append(auction)

    return render(request, 'profile.html', {'user_auctions': user_auctions})



    
