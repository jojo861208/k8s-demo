from django.shortcuts import render, redirect
from django.http.response import HttpResponse  
from django.contrib import auth
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from human.models import *
from human.forms import HumanForm, ExpertiseInlineFormSet

# Create your views here.

User = get_user_model()

class LoginView(generic.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'human/login.html')

    def post(self, request, *args, **kwargs):
        # 當使用者 POST 表單後運行這部分程式碼
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 用 auth.authenticate 來找 db 內是否有這筆帳戶資料
        user = auth.authenticate(username=username, password=password)
        
        if user and user.is_active: # 判斷 user 是否存在，且沒有被凍結
            # 允許登入
            auth.login(request, user)
            if request.GET.get('next'):
                # 當有 next 參數時，幫忙導頁
                return redirect(request.GET.get('next'))
            return redirect(reverse_lazy('human:index')) # 進行導頁到 index
        else:     
            # 不允許登入
            context = {
                "msg": "登入失敗",
            }
            return render(request, 'human/login.html', context)


class HumanFormView(generic.UpdateView):
    model = Human
    template_name = 'human/index.html'
    form_class = HumanForm
    success_url = reverse_lazy('human:index')

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(HumanFormView, self).get_context_data(**kwargs)
        ctx['expertiseInlineFormSet'] = ExpertiseInlineFormSet(
            Human,
            instance=self.object,
        )
        return ctx

    def get_object(self):
        if Human.objects.filter(user=self.request.user).exists():
            return Human.objects.get(user=self.request.user)
        else:
            human = Human.objects.create(
                user=self.request.user,
                name=self.request.user.username,
                gender=0,
            )
            return human
            

    def form_valid(self, form):
        messages.success(self.request, '成功更新個人資料')

        formset = ExpertiseInlineFormSet(
            Human,
            self.request.POST,
            self.request.FILES,
            instance=self.object,
        )

        if formset.is_valid():
            formset.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '表單填寫錯誤')
        return super().form_invalid(form)

class CaseList(generic.ListView):
    template_name = 'human/case-list.html'
    context_object_name = 'cases' 
    paginate_by = 20 

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):
        human = Human.objects.get(user=request.user)
        
        if not human.coordinates:
            messages.warning(request, "請先設定希望工作地點座標")
            return redirect("human:index")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self): 

        human = Human.objects.get(user=self.request.user)
        return Case.objects.all().annotate(
            distance=Distance('location', human.coordinates),
            ).order_by('distance')

class CaseDetail(generic.DetailView):
    template_name = 'human/case-detail.html'
    context_object_name = 'case'

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CaseDetail, self).get_context_data(**kwargs) 
        
        return ctx

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        human = Human.objects.get(user=self.request.user)
        case = Case.objects.filter(id=pk).annotate(
            distance=Distance('location', human.coordinates)).first()
        return case

class ItemHumanCreate(generic.View):

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk1 = kwargs['pk']
        case = Case.objects.get(id=pk1)
        pk2 = kwargs['pk2']
        item = Item.objects.get(id=pk2)
        moneyRequired = request.POST.get("moneyRequire")
        human = Human.objects.get(user=self.request.user)
        if moneyRequired:
            if not ItemHuman.objects.filter(human=human, item=item).exists():
                ItemHuman.objects.create(
                    human=human, 
                    item=item,
                    moneyRequired=moneyRequired,
                )
                messages.success(self.request, '成功提交申請')
            else:
                messages.warning(self.request, '您已提交過申請')
        else:
            messages.warning(self.request, '表單填寫錯誤')

        url = reverse_lazy('human:case-detail', kwargs={'pk': pk1})
        return redirect(url)

class ItemHumanList(generic.ListView):
    template_name = 'human/ihs-list.html'
    context_object_name = 'ihs' 
    paginate_by = 20

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self): 
        human = Human.objects.get(user=self.request.user)
        return ItemHuman.objects.filter(human=human)

class ItemHumanUpdate(generic.View):

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        ih = ItemHuman.objects.get(id=pk)
        moneyRequired = request.POST.get("moneyRequire")

        if moneyRequired:
            ih.moneyRequired = moneyRequired
            ih.save()
            messages.success(self.request, '更新成功')
        else:
            messages.warning(self.request, '表單填寫錯誤')

        url = reverse_lazy('human:itemhuman-list')
        return redirect(url)

class ItemHumanAction(generic.View):

    @method_decorator(login_required(login_url='/human/login/'))
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        ih = ItemHuman.objects.get(id=pk)
        
        agree = request.POST.get("agree")
        delete = request.POST.get("delete")
        
        if agree:
            ih.agree = True
            ih.save()
            messages.success(self.request, '已同意: %s %s' % (ih.item.case.name, ih.item.skill))

        if delete:
            ih.delete()
            messages.success(self.request, '刪除成功')
            
        url = reverse_lazy('human:itemhuman-list')
        return redirect(url)

def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('human:index'))  # 登出後導頁到 index 

def register(request):
    if request.POST:
        # 當使用者 POST 表單後運行這部分程式碼
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if not User.objects.filter(username=username).exists(): # 判斷是否 username 有存在 db 內
                user = User.objects.create(
                    username=username,
                    password=make_password(password1), # 密碼加密
                )
                human = Human.objects.create(
                    user=user,
                    name=username,
                    gender=0,
                )
                return redirect(reverse_lazy('human:login'))  # 登出後導頁到 login
            else:
                context = {
                    "msg": "此使用者帳號已被申請過",
                }
                return render(request, 'human/register.html', context)
        else:
            context = {
                "msg": "一次密碼與二次密碼不相同",
            }
            return render(request, 'human/register.html', context)
    return render(request, 'human/register.html')

