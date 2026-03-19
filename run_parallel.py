import subprocess
import sys

def run_parallel_tests():
    """Запуск тестов параллельно на разных браузерах"""
    
    print("=" * 60)
    print("Запуск тестов параллельно в 2 потока")
    print("=" * 60)
    
    # Команды для запуска
    commands = [
        # Chrome тесты (1 поток)
        ["pytest", "-n", "1", "--browser=chrome", "--headless", "tests/test_cart.py", "tests/test_favorites.py"],
        # Firefox тесты (1 поток)
        ["pytest", "-n", "1", "--browser=firefox", "--headless", "tests/test_filter.py", "tests/test_search.py", "tests/test_product_details.py"],
    ]
    
    # Запускаем процессы параллельно
    processes = []
    for cmd in commands:
        print(f"\nЗапуск: {' '.join(cmd)}")
        processes.append(subprocess.Popen(cmd))
    
    # Ждем завершения всех процессов
    for i, process in enumerate(processes):
        process.wait()
        print(f"Процесс {i+1} завершен с кодом {process.returncode}")
    
    print("\n" + "=" * 60)
    print("Все параллельные тесты завершены")
    print("=" * 60)

if __name__ == "__main__":
    run_parallel_tests()