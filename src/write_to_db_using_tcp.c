#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <sys/time.h>

#define SERVER "127.0.0.0"
#define PORT 8086

int main() {
    // Configuration
    const char *org = "Agnikul";
    const char *bucket = "test_bucket";
    const char *token = "sOUQsISLh_NrZMiDLYOrd9tnhgD-GRppfuQus1WQfbsW_FOMVUIm_c-2o428MOySuUyLZixLkSwl6jWUA_9b_Q==";  // Replace with your actual token
    const char *measurement = "sine_wave";
    const char *device = "sensor1";
    double value = 6.5;

    // Get current time in nanoseconds since epoch
    struct timeval tv;
    gettimeofday(&tv, NULL);
    long long timestamp = (long long)tv.tv_sec * 1000000000LL + (long long)tv.tv_usec * 1000LL;

    // Prepare data to be written
    char data[256];
    snprintf(data, sizeof(data), "%s,device=%s value=%.2f %lld", measurement, device, value, timestamp);

    // Prepare HTTP POST request
    char request[1024];
    snprintf(request, sizeof(request),
        "POST /api/v2/write?org=%s&bucket=%s&precision=ns HTTP/1.1\r\n"
        "Host: %s:%d\r\n"
        "Authorization: Token %s\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: %zu\r\n"
        "\r\n"
        "%s",
        org, bucket, SERVER, PORT, token, strlen(data), data);

    // Create socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Server address
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, SERVER, &server_addr.sin_addr) <= 0) {
        perror("inet_pton");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Connect to server
    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Send request
    if (send(sockfd, request, strlen(request), 0) < 0) {
        perror("send");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    printf("data_written\n");

    // Receive response
    char response[4096];
    int bytes_received = recv(sockfd, response, sizeof(response) - 1, 0);
    if (bytes_received < 0) {
        perror("recv");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Null-terminate and print the response
    response[bytes_received] = '\0';
    printf("Response:\n%s\n", response);

    // Clean up
    close(sockfd);
    return 0;
}
