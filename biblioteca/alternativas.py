# Editar el martes 1
"""
class Bibliotecario(ListView):
   
    Vista para ver panel de control del bibliotecario
    

    model = Libro
    template_name_suffix = "_bibliotecario"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore
        if self.request.user.get_username() == "bibliotecario":
            context = super().get_context_data(**kwargs)
            context["numeroPrestamos"] = Prestamo.objects.count()
            context["numeroDisponibles"] = Libro.objects.filter(
                disponibilidad="D"
            ).count()
            context["librosNoDevueltos"] = Prestamo.objects.filter(
                fecha_devolucion__lt=datetime.now()
            )
            context["librosAdevolver"] = Prestamo.objects.filter(
                fecha__devolucion__gt=datetime.now() - timedelta(days=7)
            )
            context["topLibros"] = Libro.objects.filter(valoracion__gte=4)
            context["librosDisponibles"] = Libro.objects.filter(disponibilidad="D")
            context["librosReservados"] = Libro.objects.filter(disponibilidad="R")
            return context

class ValorarLibro(View):
    def get(self,request,pk):
        libro = get_object_or_404(Libro, pk=pk)
        prestamo=Prestamo.objects.filter(libro=libro,usuario=request.user)
        return render(self.request, "biblioteca/libro_valorar.html", {"prestamo": prestamo})
    def post(self,request,pk):
        libro = get_object_or_404(Libro, pk=pk)
        prestamo=Prestamo.objects.filter(libro=libro,usuario=request.user)
        valoracion=Valoracion.objects.create(
            libro=libro,
            usuario=request.user,
            valoracion=request.POST.get("rating"),
        )
        libro.rating=Valoracion.objects.filter(libro=libro).aggregate(Avg("valoracion"))
        libro.save()
        return redirect("detalles",libro.pk)
    model = Libro
    fields = ["rating"]
    template_name_suffix = "_valorar"
    success_url = reverse_lazy("listar")

    def form_valid(self, form):
        libro = Libro.objects.get(pk=self.kwargs["pk"])
        valoracion = libro.rating
        valoracion.libro = libro
        valoracion.usuario = self.request.user
        valoracion.valoracion = form.cleaned_data["rating"]
        valoracion.save()
        media = Libro.objects.aggregate(Avg())
        libro.rating=(Avg(libro.rating))
        libro.rating = (libro.rating + valoracion.rating) / len.libro.rating
        libro.valoracion
        Valoracion.objects.aggregate(
            Avg("rating")
        )
        libro.save()
        return redirect("listar", self.request.user)
class ValoracionMedia(UpdateView):
    model = Prestamo
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("listar")

    def form_valid(self, form):
        libro = Libro.objects.get(pk=self.kwargs["pk"])
        valoracion = libro.rating
        valoracion.libro = libro
        valoracion.usuario = self.request.user
        valoracion.valoracion = form.cleaned_data["rating"]
        valoracion.save()
        promedio = sum([v.valoracion for v in libro.rating.all()]) / len(
            libro.rating.all()
        )
        media = Libro.objects.aggregate(Avg())
        libro.rating = (libro.rating + valoracion.rating) / 2
        libro.valoracion
        prestamo.libro = libro
        prestamo.libro.rating, prestamo.valoracion = Valoracion.objects.aggregate(
            Avg("rating")
        )
        libro.save()
        return redirect("listar", self.request.user)

#Editar mañana 3
def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    
    Valora un libro.
    
    prestamo = Prestamo.objects.get(id=post_id)
    Valoracion.objects.filter(libro=prestamo, usuario=request.user).delete()
    prestamo.valoracion_set.create(usuario=request.user, rating=rating)
    return index(request)

#Editar mañana 4
def index(request: HttpRequest) -> HttpResponse:
    
    Render the index page.
    
    libros = Prestamo.objects.all()
    for libro in libros:
        rating = Valoracion.objects.filter(libro=libro, usuario=request.user).first()
        libro.valoracion_usuario = rating.rating if rating else 0
    return render(request, "index.html", {"posts": libros})

    Modelo que representa una valoración de un libro.
   

    libro = models.ForeignKey("Libro", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, default=0
    )

    def __str__(self):
       
        Devuelve una representación en cadena del libro valorado.
        
        return str(self.libro)
    """
