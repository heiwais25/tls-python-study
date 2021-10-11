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

<img height="400px" alt="ecdhe-curve" src="https://user-images.githubusercontent.com/20959767/136698843-1879f906-939f-47ec-9041-dca8131d3b20.png" />

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

## Authentication

### RSA

Diffie Hellman이나 ECDHE를 통해서 원하는 Key를 교환할 수 있지만 알고리즘 자체가 상대방을 인증해주지는 못한다. [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))는 단방향 암호화를 통해 인증을 가능하게 한다. RSA Algorithm을 사용하는 방법은 다음과 같다.

1. 암호화의 주체(서비스 제공자)는 Prime number p, q를 준비한다.
2. `p x q = N`을 계산
3. `p - 1`과 `q - 1`의 최소 공배수 `phi = lcm(p - 1, q - 1)`를 계산한다.
4. `phi`와 co-prime인 prime number `e`를 찾는다.
5. `e`, `phi`에 대해 modular inverse인 `d`를 계산한다.
   - `e x d = 1 (mod phi)`
6. `e`, `N`은 공개키로 사용하며 `d`는 비밀키로 사용한다.
   - 나머지 `phi`, `p`, `q`는 사용하지 않으므로 버린다.
   - [RSA-CRT](https://iacr.org/archive/ches2008/51540128/51540128.pdf) 방식에서는 `p`, `q`를 사용하여 보다 빠른 계산을 가능하게 한다.
7. 메시지를 보내는 쪽에서는 다음과 같이 power modulus를 이용해 메시지를 암호화한다.
   - `c = m^e mod N`
8. 비밀키를 가지고 있는 쪽에서는 다음과 같이 비밀키를 이용하여 복호화한다.
   - `m = e^d mod N`

RSA Algorithm은 Fermat's little theorem과 CRT(Chinese remainder theorem)을 통해 증명할 수 있다. Euler's theorem을 이용하여 증명해보일 수 있지만 이는 Message 값이 N과 서로소여야 하기 때문에 한정된 증명 방법이다. 관련된 증명 방법은 여기서 확인할 수 있다. [링크](https://en.wikipedia.org/wiki/RSA_(cryptosystem))

이 방식은 N의 값이 커질수록 해킹으로부터 안전하며 높은 RSA Number(p x q의 Bit 수 또는 Decimal 자리수)를 가지는 Semi-prime 수를 소인수분해는 대회([RSA Factoring Challenge](https://en.wikipedia.org/wiki/RSA_Factoring_Challenge)) 도 열리고 있다. 가장 최근에 소인수분해에 성공한 값은 RSA 250으로 10진수로 250자리의 수였다. 그 이상의 값들은 아직까지도 성공하지 못했다. 

RSA Number는 보통 10진수 자리를 의미하는데, 예를 들어 RSA 100은 `N(= p x q)`의 10진수 자리수가 100자리임을 의미한다. 예외적으로 다음 RSA Number들은 10진수 대신 2진수 자리를 나타낸다.

1. RSA-576
2. RSA-640
3. RSA-704
4. RSA-768
5. RSA-1024
6. RSA-1536
7. RSA-2048

RSA를 이용하여 인증을 했을 때 가질 수 있는 의문은 Public Key를 발행한 서비스가 믿을만한지 확신할 수 있는지 여부다. 사실 이전의 키 교환 알고리즘처럼 RSA Public Key를 발행한 하나의 서비스만으로는 해당 서비스를 믿을 수는 없다. 이 문제를 해결하기 위해서 사용한 것은 바로 Certificate Chain이다. 이는 인증을 담당하는 몇개의 기관들을 이용하는 것이며 서비스를 제공하는 쪽에서는 다음과 같은 과정을 통해 상위 인증 기관으로부터 인증받은 인증서를 제공한다.

1. 서비스 제공자는 자신의 Public Key를 포함한 인증서 정보를 인증 기관에 제출한다.
2. 인증 기관에서는 제공받은 **인증서 정보를 Hash 계산한 후에 자신의 비밀키를 이용하여 서명**한다.
3. 서비스 제공자는 인증 기관으로부터 받은 서명값을 인증서 정보 뒤에 추가한다.
4. 사용자가 서비스에 접근하면 제공하면 **자신의 인증서 + 인증 기관으로부터의 서명값 + 인증 기관의 인증서를 함께 제공**한다.
5. 서비스 사용자는 제공받은 인증서 정보에 포함된 인증 기관의 서명값을 인증 기관의 인증서를 이용하여 원래의 Hash 값을 알아낸다.
6. 서비스의 인증서를 Hash 계산하여 방금 얻은 Hash 값과 비교한다.
7. Hash 값이 일치하고 인증 기관이 믿을 수 있는 인증 기관으로 등록되었다면 믿을 수 있는 서비스로 여긴다.

> A라는 기관으로부터 인증을 받은 경우, A는 B로부터 인증을 받았을 수 있다. 이 관계가 Certificate Chain이며 계속해서 상위 인증 정보로 올라가다보면 Root Certificate 기관을 확인할 수 있다. Root Certificate 기관은 스스로 서명 (Self-Signed) 하였으며 브라우저나 OS에는 기본적으로 믿을 수 있는 최상위 인증 기관들에 대한 정보를 저장하고 있어 Root Certificate 기관들을 확인할 수 있다.

