import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        // Cập nhật state để render fallback UI
        return { hasError: true, error: error };
    }

    componentDidCatch(error, errorInfo) {
        // Bạn cũng có thể ghi log lỗi vào một dịch vụ báo lỗi
        this.setState({ errorInfo: errorInfo });
        console.error("Uncaught error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            // Bạn có thể render bất kỳ UI thay thế nào tùy thích
            return (
                <div style={{ padding: '20px', backgroundColor: '#f9d5d5', borderRadius: '10px' }}>
                    <h1>Oops, something went wrong.</h1>
                    <details style={{ whiteSpace: 'pre-wrap' }}>
                        {this.state.error && this.state.error.toString()}
                        <br />
                        {this.state.errorInfo.componentStack}
                    </details>
                </div>
            );
        }

        return this.props.children; 
    }
}

export default ErrorBoundary;
