# Comment out these function-based views:
# def relationship_list(request):
#     relationships = Relationship.objects.all()
#     return render(
#         request,
#         "relationship_app/relationship_list.html",
#         {"relationships": relationships},
#     )


# def relationship_detail(request, pk):
#     relationship = Relationship.objects.get(pk=pk)
#     return render(
#         request,
#         "relationship_app/relationship_detail.html",
#         {"relationship": relationship},
#     )


# def relationship_create(request):
#     # Add your implementation for relationship creation
#     pass


# def relationship_update(request, pk):
#     # Add your implementation for relationship update
#     pass


# def relationship_delete(request, pk):
#     # Add your implementation for relationship deletion
#     pass


# Comment out these class-based views:
# class RelationshipListView(ListView):
    # model = Relationship
#     template_name = "relationship_app/relationship_list.html"
#     context_object_name = "relationships"


# class RelationshipDetailView(DetailView):
    # model = Relationship
#     template_name = "relationship_app/relationship_detail.html"
#     context_object_name = "relationship"


# class RelationshipCreateView(CreateView):
#     model = Relationship
#     template_name = "relationship_app/relationship_form.html"
#     # Add your form fields here


# class RelationshipUpdateView(UpdateView):
#     model = Relationship
#     template_name = "relationship_app/relationship_form.html"
#     # Add your form fields here


# class RelationshipDeleteView(DeleteView):
#     model = Relationship
#     template_name = "relationship_app/relationship_confirm_delete.html"
#     success_url = "/"  # Update with your success URL
