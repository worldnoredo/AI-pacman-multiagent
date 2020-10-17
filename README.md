# AI-pacman-multiagent

Thuật toán:
1. Q1:reflex agent:
 - Đưa ra hệ số đánh giá cho trạng thái
  + Với ghost: khi ghost bên cạnh (d<=1), nếu ghostScare thì cộng điểm, không thì trừ (lose). Khi ghost gần (d=2), trừ điểm 
  + Với capsule: phụ thuộc vào khoảng cách để tăng điểm, càng gần càng nhiều điểm
  + Với food: dựa vào khoảng cách với food gần nhất, càng gần càng nhiều điểm
2. Q2:minimax agent:
 - Lấy giá trị lớn nhất cho pacman, giá trị nhỏ nhất cho ghost
 - Sử dụng đệ quy, maxfunction cho pacman và minfunction cho ghost
 - pacman sẽ lấy giá trị lớn nhất trong các minfunction của ghost đầu tiên
 - các ghost sẽ lấy giá trị nhỏ nhất trong các minfunction của các ghost tiếp theo. Với ghost cuối cùng sẽ là nhỏ nhất của các maxfunction của pacman
 - đệ quy đến khi kết thúc game hoặc deep = 0
3. Q3:alpha-beta agent
 - tương tự Q2
 - thêm tham số alpha, beta trong hàm maxfunction. minfunction
 - Với hàm maxfunction:
  + So sánh giá trị với beta. Lớn hơn thì dừng vòng lặp
  + gán alpha = max(alpha,point)
 - Với hàm minfunction:
  + So sánh giá trị với alpha. bé hơn thì dừng vòng lặp
  + gán beta = min(beta,point)
4. Q4:expectimaxAgent
 - hàm đệ quy
 - tương tự minimaxAgent
 - với ghost: đánh giá điểm dựa vào trung bình của các giá trị
 - với pacman: vẫn đưa ra action đạt score cao nhât
5. Q5: betterEvaluation
 - xây dựng tương tự reflex agent
 - trừ điểm theo numFood và numCapsule

 
