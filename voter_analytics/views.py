from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import pandas as pd


class VoterListView(ListView):
    model = Voter
    template_name = "voter_analytics/voter_list.html"
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Get filter values from the form
        party = (
            self.request.GET.get("party_affiliation", "").strip().upper()
        )  # Normalize input
        min_year = self.request.GET.get("min_year", "")
        max_year = self.request.GET.get("max_year", "")
        voter_score = self.request.GET.get("voter_score", "")
        v20state = self.request.GET.get("v20state", "")
        v21town = self.request.GET.get("v21town", "")
        v21primary = self.request.GET.get("v21primary", "")
        v22general = self.request.GET.get("v22general", "")
        v23town = self.request.GET.get("v23town", "")

        # Apply filter for party affiliation using icontains for partial and case-insensitive match
        if party in [
            "AA",
            "GG",
            "EE",
            "FF",
            "HH",
            "WW",
            "CC",
        ]:  # List of known two-character parties
            queryset = queryset.filter(party_affiliation=party + "")
        elif party == "":
            queryset = queryset.filter(party_affiliation__icontains=party)
        else:
            queryset = queryset.filter(party_affiliation__iexact=party + "")

        # Apply filters for year range and voter score
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        if voter_score and voter_score.isdigit():
            queryset = queryset.filter(voter_score=int(voter_score))

        # Checkboxes: Only filter if the checkbox is checked ("on")
        if v20state == "on":
            queryset = queryset.filter(v20state=True)
        if v21town == "on":
            queryset = queryset.filter(v21town=True)
        if v21primary == "on":
            queryset = queryset.filter(v21primary=True)
        if v22general == "on":
            queryset = queryset.filter(v22general=True)
        if v23town == "on":
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["years"] = list(range(1920, 2024))
        context["voter_scores"] = [0, 1, 2, 3, 4, 5]
        return context


import plotly.express as px
from django.views.generic import TemplateView


class GraphsView(TemplateView):
    template_name = "voter_analytics/graphs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Voter.objects.all()

        # Get filter values from the form
        party = self.request.GET.get("party_affiliation", "").strip().upper()
        min_year = self.request.GET.get("min_year", "")
        max_year = self.request.GET.get("max_year", "")
        voter_score = self.request.GET.get("voter_score", "")
        v20state = self.request.GET.get("v20state", "")
        v21town = self.request.GET.get("v21town", "")
        v21primary = self.request.GET.get("v21primary", "")
        v22general = self.request.GET.get("v22general", "")
        v23town = self.request.GET.get("v23town", "")

        # Apply filters
        if party:
            queryset = queryset.filter(party_affiliation__iexact=party)
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        if voter_score and voter_score.isdigit():
            queryset = queryset.filter(voter_score=int(voter_score))
        if v20state == "on":
            queryset = queryset.filter(v20state=True)
        if v21town == "on":
            queryset = queryset.filter(v21town=True)
        if v21primary == "on":
            queryset = queryset.filter(v21primary=True)
        if v22general == "on":
            queryset = queryset.filter(v22general=True)
        if v23town == "on":
            queryset = queryset.filter(v23town=True)

        # Convert queryset to DataFrame
        df = pd.DataFrame(list(queryset.values()))

        # Create graphs using Plotly
        birth_year_hist = px.histogram(
            df, x="date_of_birth", title="Year of Birth Distribution", height=600
        )
        party_pie = px.pie(
            df,
            names="party_affiliation",
            title="Party Affiliation Distribution",
            height=900,
        )

        # Histogram for Voter Participation in Elections
        participation_data = {
            "Election": [
                "2020 State Election",
                "2021 Town Election",
                "2021 Primary Election",
                "2022 General Election",
                "2023 Town Election",
            ],
            "Voters Count": [
                df["v20state"].sum() if not df.empty else 0,
                df["v21town"].sum() if not df.empty else 0,
                df["v21primary"].sum() if not df.empty else 0,
                df["v22general"].sum() if not df.empty else 0,
                df["v23town"].sum() if not df.empty else 0,
            ],
        }

        participation_df = pd.DataFrame(participation_data)
        participation_hist = px.bar(
            participation_df,
            x="Election",
            y="Voters Count",
            title="Voter Participation in Recent Elections",
            labels={"Voters Count": "Number of Voters"},
            height=600,
        )

        # Add graphs to context
        context["birth_year_hist"] = birth_year_hist.to_html()
        context["party_pie"] = party_pie.to_html()
        context["participation_hist"] = participation_hist.to_html()
        context["years"] = list(range(1920, 2024))
        context["voter_scores"] = [0, 1, 2, 3, 4, 5]
        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"
