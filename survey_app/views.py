from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .forms import NameForm
from django.views.generic import TemplateView
from django.contrib import admin
from .models import Survey,Question,Answer
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator,PageNotAnInteger

import plotly

list_of_surveys_ =['If you like GeeksforGeeks','edasdsdsds','scary move','example','lol','ela re m','kala re','aaaaaaaaaaaaaaaaa','ena','toxelidoni','3232']



class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)


@api_view(['GET', 'POST']) 
def index_view(request):
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/user_login')


    


    current_user = request.user

    if(current_user):
        surveys_created_= Survey.objects.filter(user= current_user)
        surveys_created_lists= [surveys_created_[i:i+4] for i in range(0,len(surveys_created_),4)]


        current_surveys_created_page= request.GET.get('created_page')

        paginator = Paginator(surveys_created_, 5)
        range_surveys_created = list(paginator.page_range)[0:paginator.num_pages]
        try:
            surveys_created_ = paginator.page(current_surveys_created_page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            surveys_created_ = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            surveys_created_ = paginator.page(paginator.num_pages)



        current_surveys_created_page= request.GET.get('taken_page')
        answers_query = Answer.objects.filter(user=current_user)
        surveys_list= []
        for answer_ in answers_query:
            survey_ = answer_.question.survey
            if(survey_ in surveys_list):
                continue
            else:
                surveys_list.append(survey_)
        


        paginator = Paginator(surveys_list, 5)
        range_surveys_list = list(paginator.page_range)[0:paginator.num_pages]
        
        try:
            surveys_list = paginator.page(1)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            surveys_list = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            surveys_list = paginator.page(paginator.num_pages)


        return render(request, "index.html",{'surveys_taken' : {"paginator":surveys_list,"range":range_surveys_list},'surveys_created': {"paginator":surveys_created_,"range":range_surveys_created}})     
    else:
        return HttpResponseRedirect('/user_login')


@api_view(['GET', 'POST']) 
def survey_page(request, survey_id,survey_page):
    
    try:
        survey_ = Survey.objects.get(pk= int(survey_id))
        questions_ = Question.objects.filter(survey=survey_)

        current_user = request.user
        if request.method == 'POST':
            try:
                data_req = request.data
                if(survey_page==0):
                    return Response({'error':'','pk': -1},200)
                else:
                    answer_text = data_req['body']

                    question_ = questions_[int(survey_page)-1]
                    
                    answers_query = Answer.objects.filter(question=question_,user=current_user)
                    answer_ = None
                    if(len(answers_query)==0):
                        answer_ = Answer()
                    else:
                        answer_ = answers_query[0]

                    answer_.question= question_
                    answer_.body = answer_text
                    answer_.user = current_user
                    answer_.save()
                    return Response({'error':'','pk': -1},200)
            except Exception as e:
                print(e)
                return Response({'error':str(e),'pk': -1},200)


    
        if(survey_page==0):
            return render(request, 'survey/survey.html',{'survey' : survey_,'questions_length':len(questions_),'page':survey_page})      
        else:
            question_ = questions_[int(survey_page)-1]
            answers_query = Answer.objects.filter(question=question_,user=current_user)
            answer_ = None

            if(len(answers_query)!=0):
                answer_= answers_query[0]
                return render(request, 'survey/survey.html',{'survey' : survey_,'questions_length':len(questions_),'page':survey_page,'answer':answer_,'question':questions_[int(survey_page)-1]})     
            else:
                return render(request, 'survey/survey.html',{'survey' : survey_,'questions_length':len(questions_),'page':survey_page,'question':question_,'answer':answer_})     

    except Exception as e:
        print(e)
        raise Http404(e)




def print_all_questions(survey_id):
    survey_objects_=Survey.objects.get(pk= int(survey_id))
    all_survey_questions_ = Question.objects.filter(survey=survey_objects_)
    print('START QUESTIONS_')
    for q_ in all_survey_questions_:
        print(q_.question_text)
    print("END QUESTIONS")



@api_view(['GET', 'POST'])
def delete_question(request):
    
    if request.method == 'POST':
        data_req = request.data
        # json_request_=request.json()
        id_ = data_req['id']
        question_num_ = data_req['question_number']

        
        

        try:
            survey_objects_=Survey.objects.get(pk= int(id_))
            
            all_survey_questions_ = Question.objects.filter(survey=survey_objects_)
            print('length'+str(len(all_survey_questions_)))
            question_ = all_survey_questions_[int(question_num_)-1]

            question_.delete()
        

        except IndexError:
            print('indexerror')
            Response({'error':''},200)

        except Exception as e:
           
            return Response({'error':str(e)},200)

        print('Question '+str(question_num_)+' Deleted')

        return Response({'error':''},200)
        #redirect_to_ = data_req['survey_list_page']
        #return HttpResponseRedirect(request.session['login_from'])





@api_view(['GET', 'POST'])
def delete_survey(request):
    print('delete_survey')
    if request.method == 'POST':
        data_req = request.data
        # json_request_=request.json()
        id_ = data_req['id']
        
        survey_objects_=Survey.objects.get(pk= int(id_))
        all_survey_questions_ = Question.objects.filter(survey=survey_objects_)


        try:
            if(survey_objects_):
                survey_objects_.delete()
            for question_ in all_survey_questions_:
                question_.delete()
        except Exception as e:
            Response({'error':str(e),'pk': -1},200)
        
            
        return Response(200)
        #redirect_to_ = data_req['survey_list_page']
        #return HttpResponseRedirect(request.session['login_from'])



@api_view(['GET', 'POST'])
def get_questions_length(request):
    print('delete_survey')
    if request.method == 'POST':
        try:
            data_req = request.data
            # json_request_=request.json()
            id_ = data_req['id']
            
            survey_objects_=Survey.objects.get(pk= int(id_))
            all_survey_questions_ = Question.objects.filter(survey=survey_objects_)
        
        
        except Exception as e:
            return Response(404)
        
            
        return Response({'error':'','length': str(len(all_survey_questions_))},200)



@api_view(['GET', 'POST'])
def survey_creator(request,survey_id =-1 ,page=0):
    
    if request.method == 'POST':
        print('POST')
        data_req = request.data
        
        # json_request_=request.json()
        survey_title_ = data_req['title']
        survey_desc_ = data_req['description']
        



        try:
            current_user = request.user
        #print(survey_question_)


            if(survey_id!=-1):
                survey_new =Survey.objects.get(pk= int(survey_id))
                question_new = Question.objects.filter(survey=survey_new)
                
                if(page<=len(question_new) and page!=0):

                    question_new = question_new[page-1]
                elif(page>len(question_new)):
                    question_new = Question()
                else:
                    pass
            else:
                
                survey_new = Survey()


            #question_new = Question()

            
            

            
            #survey_new = Survey()
            survey_new.name = survey_title_
            survey_new.is_published = True
            survey_new.need_logged_user = False
            survey_new.display_by_question = False
            survey_new.user = current_user
            survey_new.description = survey_desc_
            


            if(page!=0):
                survey_question_ = json.loads(data_req['question'])
                question_new.type = survey_question_['type']
                if('choices' in survey_question_):
                    question_new.choices = survey_question_['choices']

                question_new.question_text= survey_question_['question']
                print('itsin page:'+str(page)+' '+str(question_new.question_text))
                

                #print(question_new.question_text)
                question_new.survey = survey_new

                question_new.save()
                print_all_questions(survey_id)


                    
            survey_new.save()
            #question_new.save()
            
        except Exception as e:
            #print('elelelelelelel')
            print(e)
            
            return Response({'error':str(e),'pk': -1},200)
        else:
            return Response({'error':"",'pk': str(survey_new.pk)},200)


    

    if(survey_id ==-1):
        survey_new = Survey()
        

        survey_new.name = '<Edit title Here>'
        survey_new.description = '<Edit Description Here>'
        survey_new.pk = -1
        return render(request, 'survey/survey_create.html',{'survey' : survey_new,'page':page,'questions_length':0,'question':None})
    elif(page==0):
        try:
            survey_new = Survey.objects.get(pk= int(survey_id))
            questions_ = Question.objects.filter(survey=survey_new)

            return render(request, 'survey/survey_create.html',{'survey' : survey_new,'questions_length':len(questions_),'page':page}) 
        except Exception as e:
            print(e)
            raise Http404(e)
    else:
        questions_ = None
        try:
            survey_new = Survey.objects.get(pk= int(survey_id))
            questions_ = Question.objects.filter(survey=survey_new)


            if(page<=len(questions_)):

                
                
                return render(request, 'survey/survey_create.html',{'survey' : survey_new,'page':page,'questions_length':len(questions_),'question':questions_[int(page)-1]})    
            else:
                return render(request, 'survey/survey_create.html',{'survey' : survey_new,'page':page,'questions_length':len(questions_)}) 

        except Exception as e:
            print(e)
            raise Http404(e)

        
        
        


    #survey_new = Survey()
    #survey_new.name = '<Edit title Here>'
    #survey_new.description = '<Edit Description Here>'

    #return render(json_request_, 'survey/survey_create.html',{'survey' : survey_new,'page':page})








def survey_list(request,page):
    survey_objects_ = Survey.objects.all()

    list_of_surveys = [str(s_.name)+' , '+str(s_.description) for s_ in survey_objects_]
    list_of_surveys = list(survey_objects_)
    #list_of_surveys = list_of_surveys_
    if(len(list_of_surveys)==0):
        list_of_surveys= []
        number_of_pages_ = 1
        page_list_=[1]
    else:
        number_of_pages_ = (len(list_of_surveys)-1)//5 +1
        page_list_ =[ i+1  for i in range(number_of_pages_)]
    

    if(page==1):
        list_of_surveys = list_of_surveys[:5]
    else:
        list_of_surveys = list_of_surveys[(page-1)*5:page*5]
    return render(request, 'survey/list.html',{ 'surveys': list_of_surveys,'number_of_pages':page_list_,'current_page':page})

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'index.html', {'form': form})


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")




@api_view(['GET', 'POST'])
def survey_visualization(request,survey_id =-1 ,page=0):

    try:
        survey_ = Survey.objects.get(pk= int(survey_id))
        questions_ = Question.objects.filter(survey=survey_)

        current_user = request.user
        

    
        if(page==0):
            append_to_viz= []
            if('append_to_viz' in request.GET):
                splited_ = request.GET['append_to_viz'].split(',')
                if(len(splited_)==1):
                    append_to_viz.append(splited_[0])
                else:
                    append_to_viz = splited_
            
            questions_to_visualize = [Question.objects.get(pk= int(i_)) for i_ in  append_to_viz]
            return render(request, 'survey/survey_viz.html',{'survey' : survey_,'questions_length':len(questions_),'page':page,"viz":questions_to_visualize})      
        else:
            question_ = questions_[int(page)-1]
            answers_query = Answer.objects.filter(question=question_,user=current_user)
            answer_ = None


            append_to_viz= []
            if('append_to_viz' in request.GET):
                splited_ = request.GET['append_to_viz'].split(',')
                if(len(splited_)==1):
                    append_to_viz.append(splited_[0])
                else:
                    append_to_viz = splited_
            
            questions_to_visualize = [Question.objects.get(pk= int(i_)) for i_ in  append_to_viz]

            

            viz_=None
            if('viz' in request.GET and len(questions_to_visualize)==2):
                viz_ = get_plot_plotly(questions_to_visualize)

                

            
            if(len(answers_query)!=0):
                answer_= answers_query[0]
                return render(request, 'survey/survey_viz.html',{'survey' : survey_,"html_plot":viz_,
                    'questions_length':len(questions_),'page':page,"viz":questions_to_visualize,'answer':answer_,'question':questions_[int(page)-1]})     
            else:
                return render(request, 'survey/survey_viz.html',{'survey' : survey_,"html_plot":viz_,
                    'questions_length':len(questions_),'page':page,'question':question_,'answer':answer_,"viz":questions_to_visualize})     

    except Exception as e:
        print(e)
        raise Http404(e)




def get_plot_plotly(questions):
    import plotly.graph_objs as go
    import plotly.offline as opy

    try:
        x_ = Answer.objects.filter(question=questions[0])
        y_ = Answer.objects.filter(question=questions[1])


        if(len(questions)==2 and all(question_.type in ["integer","float"] for question_ in questions)):
            x_ = [float(ans_.body) for ans_ in x_]
            y_ = [float(ans_.body) for  ans_ in y_]
            print(x_)
            print(y_)
            trace1 = go.Scatter(x=x_, y=y_, marker={'color': 'red', 'symbol': 104, 'size': 10},
                                mode="lines",  name='1st Trace')
            data=go.Data([trace1])
            layout=go.Layout(title="Meine Daten", xaxis={'title':questions[0].question_text}, yaxis={'title':questions[1].question_text})
            figure=go.Figure(data=data,layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')
            return div
        else:
            return None
    except Exception as e:
        print(e)
    return None
