
@api_view(["POST"])
def professional_signin(request):
    email = request.data['email']
    password = request.data['password']
    data = {
        'username': email,
        'password': password
    }
    data = requests.post(f'{request.scheme}://{request.META["HTTP_HOST"]}/api/token/get/', json=data).json()
    user = User.objects.get(email=email)
    pro = Professional.objects.get(user_id = user.id)
    data['user'] = {
        'id' : user.id,
        'email' : email
    }
    data['pro'] = ProfessionalSerializer(pro, many=False).data
    response = Response(data)
    response.set_cookie('access', data["access"])
    response.set_cookie('refresh', data["refresh"])
    response.set_cookie('user', user.id)
    return response

@api_view(["POST"])
def company_signin(request):
    email = request.data['email']
    password = request.data['password']
    data = {
        'username': email,
        'password': password
    }
    data = requests.post(f'{request.scheme}://{request.META["HTTP_HOST"]}/api/token/get/', json=data).json()
    user = User.objects.get(email=email)
    company = Company.objects.get(user_id = user.id)
    data['user'] = {
        'id': user.id,
        'email': email
    }
    data['company'] = CompanySerializer(company, many=False).data
    response = Response(data)
    response.set_cookie('access', data["access"])
    response.set_cookie('refresh', data["refresh"])
    response.set_cookie('user', user.id)
    return response
