from django.db.models.base import Model as Model
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,TemplateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import  Q
from django.contrib.auth import get_user_model
from .models import Course, Videos, QuizProfile, Quiz, Question, HomePage
from .forms import QuizForm


class HomeView(TemplateView):
    template_name = 'article/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['courses'] = Course.objects.active()[0:5]
        context['home']    = HomePage.objects.first()
        # context['banner1_slug']    = HomePage.objects.first().banner_course.slug
        # context['banner2_slug']    = HomePage.objects.first().banner2_course.slug
        return context


class CourseListView(ListView):
    
    queryset = Course.objects.active()
    paginate_by = 6
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    def get_object(self):
        global course_query
        course_query   = get_object_or_404(Course.objects.active(), slug=self.kwargs["slug"]) #course_slug
        return course_query 

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_has_this_course"] = False
            if course_query  in  self.request.user.courses.all():
                context["user_has_this_course"] = True
        return context
    
    # def get_queryset(self):
    #     if self.request.method == 'GET':
    #         queryset = get_object_or_404(Course, slug = self.kwargs["slug"]) 
    #         return queryset


class VideoDetailView(DetailView):

    template_name = "article/course_detail.html"
    model = Course
    
    def get_object(self):
        # return get_object_or_404(Videos, id=self.kwargs["pk"])
        global  course_query 
        # course_query   = get_object_or_404(Course.objects.active(), slug=self.kwargs["slug"]) #course_slug
        # course_query   = get_object_or_404(Course.objects.select_related("videos").active(), slug=self.kwargs["slug"]) #course_slug 
        course_query   = get_object_or_404(Course.objects.prefetch_related("videos").filter(is_active=True), slug=self.kwargs["slug"]) #course_slug  
        # course_query   = Course.objects.select_related("course").get(pk = self.kwargs["pk"], slug=self.kwargs["video_slug"]).videofile
        return course_query 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        pk = self.kwargs.get("pk", None) #get pk of urlConf
        if  pk :
            # context['video_file'] = get_object_or_404(Videos,pk = self.kwargs["pk"], slug=self.kwargs["video_slug"]  ).videofile
            
            video_query = course_query.videos.get(pk = self.kwargs["pk"], slug=self.kwargs["video_slug"])
            
            user_has_this_course = False
            if self.request.user and self.request.user.is_authenticated and course_query  in  self.request.user.courses.all():
                user_has_this_course = True
            
            if  video_query.is_free or course_query.is_free or user_has_this_course :
                context['video_file'] =  video_query.videofile
                context['is_video_page'] = True  #specify that  we are in the course page or the video page
                context['video_title'] = video_query.title
                context['video_is_free'] = video_query.is_free
                context['video_description'] = video_query.video_description
                context["user_has_this_course"] = user_has_this_course
            else :
                raise Http404
        return context


# class QuizView(LoginRequiredMixin, UpdateView):
#     template_name = 'article/quiz.html'
#     # model = QuizProfile
#     form_class = QuizForm
    
#     def get_success_url(self):
#         return reverse_lazy("courses:quiz", kwargs = {"quiz_id" : self.kwargs["quiz_id"]})
    
#     def get_object(self) -> Model:
#         global quiz 
#         quiz, created = QuizProfile.objects.get_or_create(
#             quiz=Quiz.objects.get(id=self.kwargs["quiz_id"]) , user=self.request.user
#         )
#         return quiz
    
#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs['questions'] = quiz.quiz.question.all()
#     #     return kwargs
    
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)

#         context["questions"] = quiz.quiz.question.all()
#         return context




@login_required
def quiz_view(request, quiz_id):
    
    quizprofile_query , created = QuizProfile.objects.select_related("quiz").get_or_create(
        quiz=Quiz.objects.get(id=quiz_id ), user=request.user)
    
    course_query = quizprofile_query.quiz.course
    course_id  = course_query.id
    course_slug  = course_query.slug
    
    
    if request.method == 'POST':
        if not quizprofile_query.is_done :
            if course_query not in  request.user.courses.all():
                request.user.courses.add(Course.objects.get(id=course_id))
            # questions=Question.objects.all()
            # questions = Quiz.objects.get(id=quiz_id).question.all()

            score=0
            wrong=0
            correct=0
            total=0
            user_choices = {}
            for q in quizprofile_query.quiz.question.all():
                total+=1
                print(request.POST)
                print("your choice", request.POST.get(str(q.pk)))
                print("ans", q.ans)
                print()
                # user_choices[request.POST.get(str(q.pk))] = q.ans
                # user_choices[str(q.pk)] = [request.POST.get(str(q.pk)), q.ans]
                user_choices[str(q.pk)] = {"user":request.POST.get(str(q.pk)), "answer": q.ans}
                if q.ans ==  request.POST.get(str(q.pk)):
                    score+=10
                    correct+=1
                else:
                    wrong+=1
            percent = ((correct*10)/(total*10)) *100
            context = {
                'correct':correct,
                'wrong':wrong,
                'score':percent,
                'total':total,
                'question_title':    quizprofile_query.quiz.title,
                'course_slug' : course_slug
                
            }
            quizprofile_query.choices = user_choices
            quizprofile_query.corrects = correct
            quizprofile_query.incorrects = wrong
            quizprofile_query.total_score = percent
            quizprofile_query.is_done = True 
            quizprofile_query.save()
            # return render(request, 'article/quiz.html', context)
            return HttpResponseRedirect(reverse_lazy("courses:quiz", args = (quiz_id,)))
        else:
            return HttpResponseRedirect(reverse_lazy("courses:quiz", args = (quiz_id,)))
    else:
        # questions, created = QuizProfile.objects.get_or_create(
        #     quiz=Quiz.objects.get(id=quiz_id ), user=request.user)
               
        context = {
            'questions':         quizprofile_query.quiz.question.all(),
            'question_title':    quizprofile_query.quiz.title,
            'is_done' :          quizprofile_query.is_done,
            'created' :          created,
            'course_slug' :      course_slug
        }
        
        if quizprofile_query.is_done:
            context.update({
                    'correct' :      quizprofile_query.corrects,
                    'wrong':         quizprofile_query.incorrects,
                    'total_score':   quizprofile_query.total_score,
                    'user_choices' : quizprofile_query.choices
            })
        
        return render(request, 'article/quiz.html', context)



class SearchView(ListView):
    template_name = 'article/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        global search
        global searched_course_query
        search = self.request.GET.get('q', "")  #q is specified in the <input name='q'... and url: http://.../search/?q=< words > 
        searched_course_query =  Course.objects.active().filter(Q(description__icontains=search) | Q(title__icontains=search))
        return searched_course_query
    
    def get_context_data(self, **kwargs): #sending extra context
        context = super().get_context_data(**kwargs)
        context["search_title"] =  search
        context["not_find"] =    False  if  searched_course_query else True
        return context