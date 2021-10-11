# TLS study in python  

## Requirements

- `gmpy2`

	```shell
	# Mac
	brew install gmp
	brew install mpfr
	brew install libmpc
	pip install gmpy2
	# To include library path in brew in pip install
	pip install --global-option=build_ext \
		--global-option="-I/opt/homebrew/include" \
		--global-option="-L/opt/homebrew/lib" gmpy2  
	```

## Key-Exchange  
  
### ECDHE (Elliptic Curve Diffie Hellman Ephemeral)

- [Source Code](tls/keyexchange/ec.py)
- [Test Code](tests/keyexchange/test_ec.py)

키 교환을 위해 타원 곡선을 이용하는 방식이다. 기본 Diffie Hellman 알고리즘과 비슷하게 공개된 값들과 자신만이 아는 값을 통해 Key를 교환하는 것은 동일하다. 하지만, ECDHE는 단순 지수승이 아니라 타원 곡선에서 주어진 점들과 특정한 규칙을 통해 교점을 구한다.

```bash
y^2 = x^3 + ax + b
```

![Sample Graph](https://user-images.githubusercontent.com/20959767/136698843-1879f906-939f-47ec-9041-dca8131d3b20.png)

연산은 다음과 같이 정의된다. 

1. 타원 곡선을 하나 정한다.
2. 두 점이 있을 때, 두 점을 지나는 선과 곡선의 교점을 찾는다.
	- 두 점이 일치할 때에는 접선을 이용하여 교점을 찾는다.
3. 교점을 x축에 대해 대칭이동한다.
4. 이렇게 얻어진 점이 두 점을 이용해 얻어지는 다음 점이다.

키 교환 알고리즘을 위해서는 실수가 아니라 나머지 연산을 적용한 값을 이용하며 이렇게 얻어진 유한체에서의 값을 사용한다. **ECDHE를 키 교환 알고리즘을 위해 사용할 수 있는 것은 연산 횟수, 시작 값을 알 때에 최종 값을 아는 것은 쉽지만 최종 값, 초기 값만을 알고 있을 때는 연산 횟수를 알기 힘들다**는 것이다. 값이 작으면 직접 계산해 볼 수도 있겠지만 실제 사용하는 값들은 32바이트의 큰 값을 사용하기 때문에 직접 계산해서 사용된 연산 횟수를 알아내는 것은 거의 불가능에 가깝다.

키 교환 알고리즘은 다음과 같이 수행된다.

1. 키 교환에 참여하는 A, B가 각각 비밀키를 정한다.
2. 서로가 사용하는 타원 곡선의 방정식, 시작점(Generator Point)은 외부에 공개된다.
3. 시작점으로 부터 연산을 비밀키만큼 수행하고 서로에게 전달한다. 이 값도 역시 외부에 공개된다.
4. 각자가 받은 값에 대해 자신이 가진 비밀키만큼의 연산을 더 수행하면 서로가 같은 값을 갖게 된다.
