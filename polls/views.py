from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from polls.models import Question,Choice
# Create your views here.
def index(request):
    latest_question_list= Question.objects.order_by('pub_date')[:5]
    context={'latest_question_list':latest_question_list}
    return render(request,'index.html',context)

def detail(request, question_id):
    try :
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question dose not exist")

    return render(request,'detail.html',{"question":question})

def results(request, question_id):
    question= get_object_or_404(Question,pk=question_id)
    render(request,'results.html',{'question':question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'detail.html',{
            'question':p,
            'error_message':"You didn't select a choice"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponse("You're voting on question %s." % question_id)